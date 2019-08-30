'''
Predict Endpoints
'''
import json
import pandas as pd
import pickle
import random
import src.prediction.model_client as client_model
import src.prediction.model_master as master_model
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.prediction.preprocessing import preprocessing_train, preprocessing_predict
from src.util import validate_request_data

predict = Blueprint('predict', __name__)
#===============================================================================
# General
@predict.route('/', methods=['POST'])
# @jwt_required
def do_predict():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'model_type': 'str',
            'project_id': 'int',
        }
        validate_request_data(data, request_types)

        # Get the data to predict
        project = Project.find_by_id(data['project_id'])
        if not project:
            raise ValueError('Project with ID {} does not exist.'.format(data['project_id']))
        project_transactions = Transaction.query.filter_by(project_id = data['project_id']).filter_by(is_approved=False)
        if project_transactions.count() == 0:
            raise IndexError('Project has no transactions to predict.')

        # Get the appropriate active model if valid
        if data['model_type'] == 'client':
            active_model = ClientModel.find_active_for_client(project.client_id)
            if not active_model:
                raise IndexError('No predictive model has been trained for client {}.'.format(Client.find_by_id(project.client_id).name))
            lh_model = client_model.ClientPredictionModel(active_model.pickle)

            project_transactions.update({Transaction.client_model_id: active_model.id})
            project_transactions.update({Transaction.master_model_id: None})
        elif data['model_type'] == 'master':
            active_model = MasterModel.find_active()
            if not active_model:
                raise IndexError('No master model has been trained or is active.')
            lh_model = master_model.MasterPredictionModel(active_model.pickle)

            project_transactions.update({Transaction.client_model_id : None})
            project_transactions.update({Transaction.master_model_id :active_model.id})
        else:
            raise ValueError('Invalid model type.')

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
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        return jsonify(response), 400
    return jsonify(response), 201
