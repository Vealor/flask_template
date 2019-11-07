'''
Master Model Endpoints
'''
import json
import pandas as pd
import pickle
import random
import src.prediction.model_master as mm
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.prediction.preprocessing import preprocessing_train, preprocessing_predict
from src.prediction.database import *
from src.util import get_date_obj_from_str, validate_request_data
from src.wrappers import has_permission, exception_wrapper

master_models = Blueprint('master_models', __name__)
#===============================================================================
# Get all master models
@master_models.route('/', defaults={'id':None}, methods=['GET'])
@master_models.route('/<path:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
def get_master_models(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = MasterModel.query
    if id:
        query = query.filter_by(id=id)
        if not query.first():
            raise ValueError("No master model with ID {} exists.".format(id))

    # Set ORDER
    query = query.order_by('id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)


    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# Train a new master model.
@master_models.route('/train/', methods=['POST'])
# @jwt_required
@exception_wrapper()
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
        raise ValueError('Invalid Train Data date range.')
    if test_start >= test_end:
        raise ValueError('Invalid Test Data date range.')
    if not (train_end < test_start or test_end < train_start):
        raise ValueError('Train and test data ranges overlap.')

    # pre-build model dictionary
    model_data_dict = {
        'train_data_start': train_start,
        'train_data_end': train_end,
        'pickle': pickle.dumps(None),
        'hyper_p': {}
    }

    # At this point, all database independent checks have been perfrm'd
    # Now, database dependent checks begin

    # validate if pending mode, stop on exist
    if MasterModel.query.filter_by(status=Activity.pending.value).all():
        raise ValueError('A pending master model exists.')

    # validate sufficient transactions for training
    transaction_count = Transaction.query.filter_by(is_approved=True).count()
    if transaction_count < 10000:
        raise ValueError('Not enough data to train a master model. Only {} approved transactions. Requires >= 10,000 approved transactions.'.format(transaction_count))

    # create placeholder model
    entry = MasterModel(**model_data_dict)
    db.session.add(entry)
    db.session.flush()
    model_id = entry.id
    lh_model = mm.MasterPredictionModel()
    transactions = Transaction.query

    # Get the required transactions and put them into dataframes
    train_transactions = transactions.filter(Transaction.modified.between(train_start,train_end)).filter_by(is_approved=True)
    train_entries = transactions_to_dataframe(train_transactions)

    test_transactions = transactions.filter(Transaction.modified.between(test_start,test_end)).filter_by(is_approved=True)
    test_entries = transactions_to_dataframe(test_transactions)

    # Training =================================
    data_train = preprocessing_train(data_train)

    target = "Target"
    predictors = list(set(data_train.columns) - set([target]))
    lh_model.train(data_train,predictors,target)

    # Update the model entry with the hyperparameters and pickle
    entry.pickle = lh_model.as_pickle()
    entry.hyper_p = {'predictors': predictors, 'target': target}

    # Output validation data results, used to assess model quality
    # Positive -> (Target == 1)
    data_valid = preprocessing_predict(data_valid,predictors,for_validation=True)
    performance_metrics = lh_model.validate(data_valid,predictors,target)
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
        performance_metrics_old = lh_model_old.validate(data_valid,predictors,target)
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

    # Send an email here?
    # ==================

    db.session.commit()
    response['payload']['performance_metrics'] = performance_metrics
    response['payload']['model_id'] = model_id
    response['message'] = 'Model trained and created.'

    return jsonify(response), 201

#===============================================================================
# Predict transactions for a project using the active master
@master_models.route('/predict/', methods=['POST'])
# @jwt_required
@exception_wrapper()
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
    project_transactions = Transaction.query.filter_by(project_id = data['project_id']).filter_by(is_approved=False)
    if project_transactions.count() == 0:
        raise ValueError('Project has no transactions to predict.')

    # Get the appropriate active model if valid
    active_model = MasterModel.find_active()
    if not active_model:
        raise ValueError('No master model has been trained or is active.')
    lh_model = mm.MasterPredictionModel(active_model.pickle)

    # indicate that the predictions were generated by a master model
    project_transactions.update({Transaction.client_model_id : None})
    project_transactions.update({Transaction.master_model_id :active_model.id})

    predictors = active_model.hyper_p['predictors']

    # TODO: fix separation of data so that prediction happens on transactions with IDs
    # Can't assume that final zip lines up arrays properly
    entries = [entry.serialize['data'] for entry in project_transactions]
    df_predict = pd.read_json('[' + ','.join(entries) + ']',orient='records')
    df_predict = preprocessing_predict(df_predict, predictors)

    # Get probability of each transaction being class '1'
    probability_recoverable = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]

    project_transactions.update({Transaction.is_predicted : True})
    for tr,pr in zip(project_transactions,probability_recoverable):
        tr.recovery_probability = pr

    db.session.commit()

    response['message'] = 'Prediction successful. Transactions have been marked.'

    return jsonify(response), 201

#===============================================================================
# Delete a master model
@master_models.route('/<path:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
def delete_master_model(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = MasterModel.find_by_id(id)
    if not query:
        raise ValueError('Master model ID {} does not exist.'.format(id))
    if query.status == Activity.active:
        raise ValueError('Master model ID {} is currently active. Cannot delete.'.format(id))

    model = query.serialize
    db.session.delete(query)
    db.session.commit()

    response['message'] = 'Deleted Master model ID {}'.format(model['id'])
    response['payload'] = [model]

    return jsonify(response), 200
