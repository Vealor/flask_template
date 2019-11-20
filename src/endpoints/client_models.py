'''
Client Model Endpoints
'''
import json
import pandas as pd
import pickle
import random
import src.prediction.model_client as cm
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user
from src.errors import *
from src.models import *
from src.prediction.preprocessing import preprocess_data, transactions_to_dataframe
from src.util import get_date_obj_from_str, validate_request_data, send_mail
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
# Check if a pending model exists
@client_models.route('/has_pending/', methods=['GET'])
# @jwt_required
@exception_wrapper()
def has_pending():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    if 'client_id' not in args.keys():
        raise InputError('Client ID must be specified in arguments')

    response['payload'] = { 'is_pending': (ClientModel.find_pending_for_client(args['client_id']) != None) }
    return jsonify(response), 200

#===============================================================================
# Check if a model is being trained for the client
@client_models.route('/is_training/', methods=['GET'])
# @jwt_required
@exception_wrapper()
def is_training():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    if 'client_id' not in args.keys():
        raise InputError('Client ID must be specified in arguments')

    response['payload'] = { 'is_training': (ClientModel.find_training_for_client(args['client_id']) != None) }
    return jsonify(response), 200


#===============================================================================
# Train a new client model.
@client_models.route('/train/', methods=['POST'])
@jwt_required
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
    model_data_dict['client_id'] = data['client_id']

    # validate existing client projects
    client_projects = [p.id for p in Project.query.filter_by(client_id = data['client_id']).distinct()]
    if not client_projects:
        raise InputError('Client ID {} has no associated projects.'.format(data['client_id']))

    # validate if training mode, stop on exist
    if ClientModel.query.filter_by(client_id = data['client_id']).filter_by(status=Activity.training.value).all():
        raise InputError('There is currently a model in training for client ID {}.'.format(data['client_id']))

    # validate if pending mode, stop on exist
    if ClientModel.query.filter_by(client_id = data['client_id']).filter_by(status=Activity.pending.value).all():
        raise InputError('There are pending models for client ID {}.'.format(data['client_id']))

    # validate sufficient transactions for training
    #transaction_count = Transaction.query.filter(Transaction.project_id.in_(client_projects)).filter(Transaction.approved_user_id != None).count()
    transaction_count = Transaction.query.filter(Transaction.project_id.in_(client_projects)).count()
    if transaction_count < 2000:
        raise InputError('Not enough data to train a model for client ID {}. Only {} approved transactions. Requires >= 2,000 approved transactions.'.format(data['client_id'],transaction_count))

    # create placeholder model
    try:
        model_data_dict['client_id'] = data['client_id']
        entry = ClientModel(**model_data_dict)
        db.session.add(entry)
        db.session.commit()
        model_id = entry.id

        # Get the required transactions and put them into dataframes
        transactions = Transaction.query.filter(Transaction.project_id.in_(client_projects)).filter(Transaction.approved_user_id != None)
        train_transactions = transactions.filter(Transaction.modified.between(train_start,train_end))#.filter(Transaction.approved_user_id == None)
        data_train = transactions_to_dataframe(train_transactions)
        test_transactions = transactions.filter(Transaction.modified.between(test_start,test_end))#.filter(Transaction.approved_user_id != None)
        data_valid = transactions_to_dataframe(test_transactions)

        # Training =================================
        data_train = preprocess_data(data_train,preprocess_for='training')

        target = "Target"
        predictors = list(set(data_train.columns) - set([target]))
        lh_model = cm.ClientPredictionModel()
        lh_model.train(data_train, predictors, target)

        # Update the model entry with the hyperparameters and pickle
        entry.pickle = lh_model.as_pickle()
        entry.hyper_p = {'predictors': predictors, 'target': target}
        entry.status = Activity.pending

        # Output validation data results, used to assess model quality
        # Positive -> (Target == 1)
        performance_metrics = lh_model.validate(
            preprocess_data(data_valid, preprocess_for='validation', predictors=predictors), predictors, target)
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
            performance_metrics_old = lh_model_old.validate(
                preprocess_data(data_valid, preprocess_for='validation', predictors=predictors_old), predictors_old, target_old)
            model_performance_dict_old = {
                'client_model_id': active_model.id,
                'accuracy': performance_metrics_old['accuracy'],
                'precision': performance_metrics_old['precision'],
                'recall': performance_metrics_old['recall'],
                'test_data_start': test_start,
                'test_data_end': test_end
            }
            db.session.add(ClientModelPerformance(**model_performance_dict_old))

    # If exception occurs delete placholder model and raise.
    except Exception as e:
        db.session.delete(ClientModel.find_by_id(model_id))
        db.session.commit()

        # Send an email to the user
        subj = "Client model training failed."
        content = """
        <p>Sorry. Model Training for client "{}" failed. Please contact the Vancouver KPMG Lighthouse team for more information.</p>
        <ul>
        <li>Error: {}</li>
        </ul>
        """.format(Client.find_by_id(data['client_id']).name,str(e))
        send_mail(current_user.email ,subj, content)

        raise Exception("Error occured during model training: " + str(e))

    db.session.commit()

    response['payload']['performance_metrics'] = performance_metrics
    response['payload']['model_id'] = model_id
    response['message'] = 'Model trained and created.'

    # Send an email to the user
    subj = "Client model training complete."
    content = """
    <p>Please log into the ARRT application to confirm the acceptability of the model</p>
    <ul>
    <li>Model Name: {}</li>
    </ul>
    """.format(ClientModel.find_by_id(model_id).serialize['name'])
    send_mail(current_user.email ,subj, content)

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
    test_transactions = Transaction.query.filter(Transaction.modified.between(test_start,test_end)).filter(Transaction.approved_user_id != None)
    if test_transactions.count() == 0:
        raise ValueError('No transactions to validate in given date range.')
    data_valid = transactions_to_dataframe(test_transactions)
    data_valid = preprocess_data(data_valid,preprocess_for='validation',predictors=predictors)

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
def compare_active_and_pending():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    args = request.args.to_dict()
    response['payload']['can_compare'] = True

    if 'client_id' not in args.keys():
        raise InputError("Client ID is a required argument to compare client models")
    client_id = args['client_id']

    pending_model = ClientModel.find_pending_for_client(client_id)
    if not pending_model:
        raise ValueError('There is no pending model to compare to the active model.')
    else:
        response['payload']['pending_metrics'] = ClientModelPerformance.get_most_recent_for_model(pending_model.id).serialize

    active_model = ClientModel.find_active_for_client(client_id)
    if not active_model:
        response['payload']['can_compare'] = False
    else:
        response['payload']['active_metrics'] = ClientModelPerformance.get_most_recent_for_model(active_model.id).serialize

    response['message'] = 'Client model comparison complete'
    return jsonify(response), 200


#===============================================================================
# Update the active model for a client
@client_models.route('/<int:model_id>/set_active', methods=['PUT'])
# @jwt_required
@exception_wrapper()
def set_active_model(model_id):
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    args = request.args.to_dict()
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
