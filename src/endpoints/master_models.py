'''
Master Model Endpoints
'''
import datetime
import json
import pandas as pd
import pickle
import random
import src.prediction.model_master as mm
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user
from src.errors import *
from src.models import *
from src.prediction.preprocessing import preprocess_data, transactions_to_dataframe
from src.util import get_date_obj_from_str, validate_request_data, send_mail
from src.wrappers import has_permission, exception_wrapper

master_models = Blueprint('master_models', __name__)
#===============================================================================
# Get all master models
@master_models.route('/', defaults={'id':None}, methods=['GET'])
@master_models.route('/<int:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_master_models(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = MasterModel.query
    if id:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError("No master model with ID {} exists.".format(id))

    # Set ORDER
    query = query.order_by('id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)


    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# Check if master models has a model in pending status
@master_models.route('/has_pending/', methods=['GET'])
# @jwt_required
@exception_wrapper()
def has_pending():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['payload'] = { 'is_pending' : (MasterModel.find_pending() != None) }
    return jsonify(response), 200


#===============================================================================
# Check if master models has a model in pending status
@master_models.route('/is_training/', methods=['GET'])
# @jwt_required
@exception_wrapper()
def is_training():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['payload'] = { 'is_training' : (MasterModel.find_training() != None) }
    return jsonify(response), 200

#===============================================================================
# Train a new master model.
@master_models.route('/train/', methods=['POST'])
#@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def do_train():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    data = request.get_json()

    # validate input
    request_types = {
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

    # validate if training mode, stop on exist
    if MasterModel.query.filter_by(status=Activity.training.value).all():
        raise InputError('A master model is currently being trained.')

    # validate if pending mode, stop on exist
    if MasterModel.query.filter_by(status=Activity.pending.value).all():
        raise InputError('A pending master model exists.')

    # validate sufficient transactions for training
    #transaction_count = Transaction.query.filter_by(is_approved=True).count()
    transaction_count = Transaction.query.count()
    if transaction_count < 5000:
        raise InputError('Not enough data to train a master model. Only {} approved transactions. Requires >= 5,000 approved transactions.'.format(transaction_count))

    #Try to create model. If model creation fails, delete placeholder and raise Exception
    try:
        # create placeholder model
        entry = MasterModel(**model_data_dict)
        db.session.add(entry)
        db.session.flush()
        model_id = entry.id
        lh_model = mm.MasterPredictionModel()
        transactions = Transaction.query

        # Get the required transactions and put them into dataframes
        train_transactions = transactions.filter(Transaction.modified.between(train_start,train_end)) #.filter_by(is_approved=True)
        data_train = transactions_to_dataframe(train_transactions)

        test_transactions = transactions.filter(Transaction.modified.between(test_start,test_end)) #.filter_by(is_approved=True)
        data_valid = transactions_to_dataframe(test_transactions)

        # Training =================================
        data_train = preprocess_data(data_train,preprocess_for='training')

        target = "Target"
        predictors = list(set(data_train.columns) - set([target]))
        print(predictors)
        lh_model.train(data_train,predictors,target)

        # Update the model entry with the hyperparameters and pickle
        entry.pickle = lh_model.as_pickle()
        entry.hyper_p = {'predictors': predictors, 'target': target}
        entry.status = Activity.pending

        # Output validation data results, used to assess model quality
        # Positive -> (Target == 1)
        data_valid_new = preprocess_data(data_valid, preprocess_for='validation', predictors=predictors)
        performance_metrics = lh_model.validate(data_valid_new, predictors, target)
        model_performance_dict = {
            'accuracy': performance_metrics['accuracy'],
            'precision': performance_metrics['precision'],
            'recall': performance_metrics['recall'],
            'test_data_start': test_start,
            'test_data_end': test_end
        }

        # Push trained model and performance metrics
        model_performance_dict['master_model_id'] = model_id
        new_model = MasterModelPerformance(**model_performance_dict)
        db.session.add(new_model)
        # If there is no active model, set the current one to be the active one.
        active_model = MasterModel.find_active()
        if active_model:
            lh_model_old = mm.MasterPredictionModel(active_model.pickle)
            predictors_old, target_old = active_model.hyper_p['predictors'], active_model.hyper_p['target']
            data_valid_old = preprocess_data(data_valid, preprocess_for='validation', predictors=predictors_old)
            performance_metrics_old = lh_model_old.validate(data_valid_old, predictors_old, target_old)
            model_performance_dict_old = {
                'master_model_id': active_model.id,
                'accuracy': performance_metrics_old['accuracy'],
                'precision': performance_metrics_old['precision'],
                'recall': performance_metrics_old['recall'],
                'test_data_start': test_start,
                'test_data_end': test_end
            }


            new_model = MasterModelPerformance(**model_performance_dict_old)
            db.session.add(new_model)
        else:
            MasterModel.set_active(model_id)
    # If exception occurs delete placholder model and raise.
    except Exception as e:
        db.session.delete(MasterModel.find_by_id(model_id))
        db.session.commit()

        # Send an email to the user
        subj = "Master model training failed."
        content = """
        <p>Sorry. Model Training failed. Please contact the Vancouver KPMG Lighthouse team for more information.</p>
        <ul>
        <li>Error: {}</li>
        </ul>
        """.format(str(e))
        send_mail("willthompson@kpmg.ca",subj,content)

        raise Exception("Error occured during model training: " + str(e))

    db.session.commit()
    response['payload']['performance_metrics'] = performance_metrics
    response['payload']['model_id'] = model_id
    response['message'] = 'Model trained and created.'

    # Send an email to the user
    subj = "Master model training is complete!"
    content = """
    <p>Please log into the ARRT application to confirm the acceptability of the model</p>
    <ul>
    <li>Model Name: {}</li>
    </ul>
    """.format(MasterModel.find_by_id(model_id).serialize['name'])
    send_mail("willthompson@kpmg.ca",subj,content)

    return jsonify(response), 201


#===============================================================================
# Predict transactions for a project using the active master
@master_models.route('/predict/', methods=['POST'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def do_predict():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # input validation
    request_types = {
        'project_id': ['int'],
    }
    validate_request_data(data, request_types)

    # Get the data to predict
    project = Project.find_by_id(data['project_id'])
    if not project:
        raise ValueError('Project with ID {} does not exist.'.format(data['project_id']))
    project_transactions = Transaction.query.filter_by(project_id = data['project_id']).filter(Transaction.approved_user_id == None)
    if project_transactions.count() == 0:
        raise ValueError('Project has no transactions to predict.')

    # Get the appropriate active model if valid
    active_model = MasterModel.find_active()
    if not active_model:
        raise ValueError('No master model has been trained or is active.')
    lh_model = mm.MasterPredictionModel(active_model.pickle)
    predictors = active_model.hyper_p['predictors']

    # Make transaction data into a data frame
    df_predict = transactions_to_dataframe(project_transactions)
    df_predict = preprocessing_predict(df_predict, predictors)

    # Get probability of each transaction being class '1'
    # TODO: fix separation of data so that prediction happens on transactions with IDs
    probability_recoverable = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]
    project_transactions.update({Transaction.is_predicted : True})
    for tr,pr in zip(project_transactions, probability_recoverable):
        tr.recovery_probability = pr

    # indicate that the predictions were generated by a master model
    project_transactions.update({Transaction.client_model_id : None})
    project_transactions.update({Transaction.master_model_id :active_model.id})

    db.session.commit()
    response['message'] = 'Prediction successful. Transactions have been marked.'

    return jsonify(response), 201


#===============================================================================
# Validate the active master model.
@master_models.route('/validate/', methods=['POST'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def do_validate():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    data = request.get_json()

    active_model = MasterModel.find_active()
    if not active_model:
        raise ValueError('No master model has been trained or is active.')

    request_types = {
        'test_data_start_date': ['str'],
        'test_data_end_date': ['str']
    }
    validate_request_data(data, request_types)
    train_start = active_model.train_data_start.date()
    train_end = active_model.train_data_end.date()
    test_start = get_date_obj_from_str(data['test_data_start_date'])
    test_end = get_date_obj_from_str(data['test_data_end_date'])
    if test_start >= test_end:
        raise ValueError('Invalid Test Data date range.')
    if not (train_end < test_start or test_end < train_start):
        raise ValueError('Cannot validate model on data it was trained on.')

    lh_model_old = mm.MasterPredictionModel(active_model.pickle)
    predictors, target = active_model.hyper_p['predictors'], active_model.hyper_p['target']

    # Pull the transaction data into a dataframe
    test_transactions = Transaction.query.filter(Transaction.modified.between(test_start,test_end)).filter_by(is_approved=True)
    if test_transactions.count() == 0:
        raise ValueError('No transactions to validate in given date range.')
    data_valid = transactions_to_dataframe(test_transactions)
    data_valid = preprocessing_predict(data_valid,predictors,for_validation=True)

    # Evaluate the performance metrics
    performance_metrics_old = lh_model_old.validate(data_valid,predictors,target)
    model_performance_dict_old = {
        'master_model_id': active_model.id,
        'accuracy': performance_metrics_old['accuracy'],
        'precision': performance_metrics_old['precision'],
        'recall': performance_metrics_old['recall'],
        'test_data_start': test_start,
        'test_data_end': test_end
    }
    db.session.add(MasterModelPerformance(**model_performance_dict_old))
    db.session.commit()

    response['message'] = 'Model validation complete.'
    response['payload']['model_id'] = active_model.id
    response['payload']['performance_metrics'] = performance_metrics_old

    return jsonify(response), 201


#===============================================================================
# Compare active and pending models
@master_models.route('/compare/', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def compare_active_and_pending():
    response = { 'status': 'ok', 'message': '', 'payload': {} }
    data = request.get_json()

    active_model = MasterModel.find_active()
    if not active_model:
        raise ValueError('No master model has been trained or is active.')
    pending_model = MasterModel.find_pending()
    if not pending_model:
        raise ValueError('There is no pending model to compare to the active model.')

    # Get the performance metrics for the pending and active models
    active_metrics = MasterModelPerformance.get_most_recent_for_model(active_model.id).serialize
    pending_metrics = MasterModelPerformance.get_most_recent_for_model(pending_model.id).serialize

    response['payload'] = {'active_metrics': active_metrics, 'pending_metrics': pending_metrics}
    response['message'] = 'Master model comparison complete'

    return jsonify(response), 200


#===============================================================================
# Update the active master model
@master_models.route('/<int:model_id>/set_active', methods=['PUT'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def set_active_model(model_id):
    response = { 'status': 'ok', 'message': '', 'payload': {} }

    pending_model = MasterModel.find_by_id(model_id)
    if not pending_model:
        raise ValueError('There is no pending model to set as active.')
    MasterModel.set_active(model_id)
    db.session.commit()
    response['message'] = 'Active Master model set to model {}'.format(model_id)

    return jsonify(response), 200


#===============================================================================
# Delete a master model
@master_models.route('/<int:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def delete_master_model(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = MasterModel.find_by_id(id)
    if not query:
        raise NotFoundError('Master model ID {} does not exist.'.format(id))
    if query.status == Activity.active:
        raise InputError('Master model ID {} is currently active. Cannot delete.'.format(id))

    model = query.serialize
    db.session.delete(query)
    db.session.commit()

    response['message'] = 'Deleted Master model ID {}'.format(model['id'])
    response['payload'] = [model]

    return jsonify(response), 200
