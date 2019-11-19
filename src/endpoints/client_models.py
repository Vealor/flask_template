'''
Client Model Endpoints
'''
import json
import pandas as pd
import pickle
import random
import src.prediction.model_client as cm
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.errors import *
from src.models import *
from src.prediction.preprocessing import preprocessing_train, preprocessing_predict
from src.util import get_date_obj_from_str, validate_request_data
from src.wrappers import has_permission, exception_wrapper

client_models = Blueprint('client_models', __name__)
#===============================================================================
# Get all client models
@client_models.route('/', defaults={'id':None}, methods=['GET'])
@client_models.route('/<int:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_client_models(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = ClientModel.query
    if id:
        query = query.filter_by(id=id)
        if not query.first():
             raise NotFoundError("No client model with ID {} exists.".format(id))

    # If client_id is specified, then return all models for that client
    query = query.filter_by(client_id=int(args['client_id'])) if 'client_id' in args.keys() and args['client_id'].isdigit() else query
    response['payload'] = [i.serialize for i in query.all()]
    return jsonify(response), 200


#===============================================================================
# Train a new client model.
@client_models.route('/train/', methods=['POST'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def do_train():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    data = request.get_json()
    # validate input
    request_types = {
        'client_id': ['int'],
        'train_data_start_date': ['str'],
        'train_data_end_date': ['str'],
        'test_data_start_date': ['str'],
        'test_data_end_date': ['str']
    }
    validate_request_data(data, request_types)

    # validate date ranges
    train_start = get_date_obj_from_str(data['train_data_start_date'])
    train_end = get_date_obj_from_str(data['train_data_end_date'])
    test_start = get_date_obj_from_str(data['test_data_start_date'])
    test_end = get_date_obj_from_str(data['test_data_end_date'])
    if train_start >= train_end:
        raise InputError('Invalid Train Data date range.')
    if test_start >= test_end:
        raise InputError('Invalid Test Data date range.')
    if not (train_end < test_start or test_end < train_start):
        raise InputError('Train and test data ranges overlap.')

    # pre-build model dictionary
    model_data_dict = {
        'train_data_start': train_start,
        'train_data_end': train_end,
        'pickle': pickle.dumps(None),
        'hyper_p': {}
    }
    # At this point, all database independent checks have been perfrm'd
    # Now, database dependent checks begin

    # validate client existence
    if not Client.find_by_id(data['client_id']):
        raise InputError('Client ID {} does not exist.'.format(data['client_id']))

    # validate existing client projects
    client_projects = [p.id for p in Project.query.filter_by(client_id = data['client_id']).distinct()]
    if not client_projects:
        raise InputError('Client ID {} has no associated projects.'.format(data['client_id']))

    # validate if pending mode, stop on exist
    if ClientModel.query.filter_by(client_id = data['client_id']).filter_by(status=Activity.pending.value).all():
        raise InputError('There are pending models for client ID {}.'.format(data['client_id']))

    # validate sufficient transactions for training
    transaction_count = Transaction.query.filter(Transaction.project_id.in_(client_projects)).filter_by(is_approved=True).count()
    if transaction_count < 2000:
        raise InputError('Not enough data to train a model for client ID {}. Only {} approved transactions. Requires >= 2,000 approved transactions.'.format(data['client_id'],transaction_count))

    # create placeholder model
    model_data_dict['client_id'] = data['client_id']
    entry = ClientModel(**model_data_dict)
    db.session.add(entry)
    db.session.flush()
    model_id = entry.id
    lh_model = cm.ClientPredictionModel()
    transactions = Transaction.query.filter(Transaction.project_id.in_(client_projects))

    # Train the instantiated model and edit the db entry
    train_transactions = transactions.filter(Transaction.modified.between(train_start,train_end)).filter_by(is_approved=True)
    train_entries = [tr.serialize['data'] for tr in train_transactions]
    data_train = pd.read_json('[' + ','.join(train_entries) + ']',orient='records')
    data_train['Code'] = [Code.find_by_id(tr.gst_hst_code_id).code_number if tr.gst_hst_code_id else -999 for tr in train_transactions]
    print("TRAIN DATA LEN: {}".format(len(data_train)))

    test_transactions = transactions.filter(Transaction.modified.between(test_start,test_end)).filter_by(is_approved=True)
    test_entries = [tr.serialize['data'] for tr in test_transactions]
    data_valid = pd.read_json('[' + ','.join(test_entries) + ']',orient='records')
    data_valid['Code'] = [Code.find_by_id(tr.gst_hst_code_id).code_number if tr.gst_hst_code_id else -999 for tr in test_transactions]
    print("TEST DATA LEN: {}".format(len(data_valid)))

    # Training =================================
    data_train = preprocessing_train(data_train)

    target = "Target"
    predictors = list(set(data_train.columns) - set([target]))
    lh_model.train(data_train, predictors, target)

    # Update the model entry with the hyperparameters and pickle
    entry.pickle = lh_model.as_pickle()
    entry.hyper_p = {'predictors': predictors, 'target': target}

    # Output validation data results, used to assess model quality
    # Positive -> (Target == 1)
    performance_metrics = lh_model.validate(
        preprocessing_predict(data_valid, predictors, for_validation=True), predictors, target)
    model_performance_dict = {
        'accuracy': performance_metrics['accuracy'],
        'precision': performance_metrics['precision'],
        'recall': performance_metrics['recall'],
        'test_data_start': test_start,
        'test_data_end': test_end
    }

    model_performance_dict['client_model_id'] = model_id
    new_model = ClientModelPerformance(**model_performance_dict)
    db.session.add(new_model)

    # If there is an active model for this client, check to compare performance
    # Else, automatically push newly trained model to active

    active_model = ClientModel.find_active_for_client(data['client_id'])
    if active_model:
        lh_model_old = cm.ClientPredictionModel(active_model.pickle)
        predictors_old, target_old = active_model.hyper_p['predictors'], active_model.hyper_p['target']
        performance_metrics_old = lh_model_old.validate(preprocessing_predict(data_valid, predictors_old, for_validation=True), predictors_old, target_old)
        model_performance_dict_old = {
            'client_model_id': active_model.id,
            'accuracy': performance_metrics_old['accuracy'],
            'precision': performance_metrics_old['precision'],
            'recall': performance_metrics_old['recall'],
            'test_data_start': test_start,
            'test_data_end': test_end
        }
        new_model = ClientModelPerformance(**model_performance_dict_old)
        db.session.add(new_model)
    else:
        ClientModel.set_active_for_client(model_id, data['client_id'])

    # Send an email here?
    # ==================

    db.session.commit()

    response['payload']['performance_metrics'] = performance_metrics
    response['payload']['model_id'] = model_id
    response['message'] = 'Model trained and created.'

    return jsonify(response), 201

#===============================================================================
# Validate the active client model based on input ID.
@client_models.route('/validate/', methods=['POST'])
# @jwt_required
@exception_wrapper()
def do_validate():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    data = request.get_json()

    request_types = {
        'test_data_start_date': ['str'],
        'test_data_end_date': ['str'],
        'client_id': ['int']
    }
    validate_request_data(data, request_types)

    active_model = ClientModel.find_active_for_client(data['client_id'])
    if not active_model:
        raise ValueError('No client model has been trained or is active for Client ID {}'.format(data['client_id']))

    train_start = active_model.train_data_start.date()
    train_end = active_model.train_data_end.date()
    test_start = get_date_obj_from_str(data['test_data_start_date'])
    test_end = get_date_obj_from_str(data['test_data_end_date'])
    if test_start >= test_end:
        raise ValueError('Invalid Test Data date range.')
    if not (train_end < test_start or test_end < train_start):
        raise ValueError('Cannot validate model on data it was trained on.')

    lh_model_old = cm.ClientPredictionModel(active_model.pickle)
    predictors, target = active_model.hyper_p['predictors'], active_model.hyper_p['target']

    # Pull the transaction data into a dataframe
    test_transactions = Transaction.query.filter(Transaction.modified.between(test_start,test_end)).filter_by(is_approved=True)
    if test_transactions.count() == 0:
        raise ValueError('No transactions to validate in given date range.')
    test_entries = [tr.serialize['data'] for tr in test_transactions]
    test_entries = pd.read_json('[' + ','.join(test_entries) + ']',orient='records')
    test_entries['Code'] = [Code.find_by_id(tr.gst_hst_code_id).code_number if tr.gst_hst_code_id else -999 for tr in test_transactions]

    data_valid = pd.read_json('[' + ','.join(test_entries) + ']',orient='records')
    data_valid = preprocessing_predict(data_valid,predictors,for_validation=True)

    # Evaluate the performance metrics
    performance_metrics_old = lh_model_old.validate(data_valid,predictors,target)
    model_performance_dict_old = {
        'client_model_id': active_model.id,
        'accuracy': performance_metrics_old['accuracy'],
        'precision': performance_metrics_old['precision'],
        'recall': performance_metrics_old['recall'],
        'test_data_start': test_start,
        'test_data_end': test_end
    }
    db.session.add(ClientModelPerformance(**model_performance_dict_old))
    db.session.commit()

    response['message'] = 'Model validation complete.'
    response['payload']['model_id'] = active_model.id
    response['payload']['performance_metrics'] = performance_metrics_old

    return jsonify(response), 201


#===============================================================================
# Compare active and pending models
@client_models.route('/compare/', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def compare_active_and_pending():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    data = request.get_json()

    request_types = {
        'test_data_start_date': ['str'],
        'test_data_end_date': ['str'],
        'client_id': ['int']
    }
    validate_request_data(data, request_types)
    active_model = ClientModel.find_active_for_client(data['client_id'])
    if not active_model:
        raise ValueError('No master model has been trained or is active.')
    pending_model = ClientModel.find_pending_for_client(data['client_id'])
    if not pending_model:
        raise ValueError('There is no pending model to compare to the active model.')

    test_start = get_date_obj_from_str(data['test_data_start_date'])
    test_end = get_date_obj_from_str(data['test_data_end_date'])

    # Check if date range is acceptable for comparing the two models
    if test_start >= test_end:
        raise ValueError('Invalid Test Data date range.')
    if not (active_model.train_data_end.date() < test_start or test_end < active_model.train_data_start.date()):
        raise ValueError('Cannot validate active model on data it was trained on.')
    if not (pending_model.train_data_end.date() < test_start or test_end < pending_model.train_data_start.date()):
        raise ValueError('Cannot validate pending model on data it was trained on.')

    # Pull the validation transaction data into a dataframe
    test_transactions = Transaction.query.filter(Transaction.modified.between(test_start,test_end)).filter_by(is_approved=True)
    if test_transactions.count() == 0:
        raise ValueError('No transactions to validate in given date range.')
    test_entries = [tr.serialize['data'] for tr in test_transactions]
    test_entries = pd.read_json('[' + ','.join(test_entries) + ']',orient='records')
    test_entries['Code'] = [Code.find_by_id(tr.gst_hst_code_id).code_number if tr.gst_hst_code_id else -999 for tr in test_transactions]

    performance_metrics = {}
    for model in [active_model, pending_model]:
        lh_model = cm.ClientPredictionModel(model.pickle)
        predictors, target = model.hyper_p['predictors'], model.hyper_p['target']
        performance_metrics[model.id] = lh_model.validate(preprocessing_predict(test_entries,predictors,for_validation=True),predictors,target)

    response['message'] = 'Client model comparison complete'
    response['payload'] = performance_metrics

    return jsonify(response), 200


#===============================================================================
# Update the active model for a client
@client_models.route('/<int:model_id>/set_active', methods=['PUT'])
# @jwt_refresh_token_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def set_active_model(model_id):
    response = { 'status': 'ok', 'message': '', 'payload': {} }

    pending_model = ClientModel.find_by_id(model_id)
    client_id = pending_model.client_id
    if not Client.find_by_id(client_id):
        raise NotFoundError("Client ID {} does not exist.".format(client_id))
    if not pending_model:
        raise ValueError('There is no pending model to compare to the active model.')
    ClientModel.set_active_for_client(model_id, client_id)
    db.session.commit()
    response['message'] = 'Active model for Client ID {} set to model {}'.format(client_id, model_id)

    return jsonify(response), 200


#===============================================================================
# Delete a client model
@client_models.route('/<int:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def delete_client_model(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = ClientModel.find_by_id(id)
    if not query:
        raise NotFoundError('Client model ID {} does not exist.'.format(id))
    if query.status == Activity.active:
        raise InputError('Client model ID {} is currently active. Cannot delete.'.format(id))

    model = query.serialize
    db.session.delete(query)
    db.session.commit()

    response['message'] = 'Deleted Client model ID {}'.format(model['id'])
    response['payload'] = [model]

    return jsonify(response), 200
