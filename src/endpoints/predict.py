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
def do_predict():
    response = { 'status': '', 'message': '', 'payload': {} }
    data = request.get_json()

    if request.method == 'POST':

        # data type dictionary
        request_types = {
            'MODEL_TYPE': 'str',
            'PROJECT_ID': 'int',
            }

        # validate input
        try:
            # Do some checks on the input itself.
            validate_request_data(data, request_types)

            if data['MODEL_TYPE'] not in ['client','master']:
                raise ValueError("ERROR: Invalid model type. Must be 'client' or 'master'.")

            # Get the data to predict
            project = Project.find_by_id(data['PROJECT_ID'])
            if not project:
                raise IndexError("ERROR: Project not found in database.")
            project_transactions = Transaction.query.filter_by(project_id = data['PROJECT_ID']).filter_by(is_approved=False).all()
            if len(project_transactions) == 0:
                raise IndexError("ERROR: Project has no transactions to predict.")

            # Get the appropriate active model
            if data['MODEL_TYPE'] == 'client':
                active_model = ClientModel.find_active_for_client(project.client_id)
                if not active_model:
                    raise IndexError('ERROR: No predictive model has been trained for client \'{}\'.'.format(Client.find_by_id(project.client_id).name))
                lh_model = client_model.ClientPredictionModel(active_model.pickle)
            else:
                active_model = MasterModel.find_active()
                if not active_model:
                    raise IndexError('ERROR: No master model has been trained')
                lh_model = master_model.MasterPredictionModel(active_model.pickle)
            predictors = active_model.hyper_p['predictors']

            entries = [entry.serialize['data'] for entry in project_transactions]
            df_predict = pd.read_json('[' + ','.join(entries) + ']',orient='records')
            df_predict = preprocessing_predict(df_predict, predictors)

            # Get probability of each transaction being class '1'
            probability_recoverable = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]

            # Modify the appropriate info in the transactions table
            print('here')
            for tr,pr in zip(project_transactions,probability_recoverable):
                tr.update_prediction({
                    data['MODEL_TYPE']+"_model_id":active_model.id,
                    "recovery_probability":pr
                    })
            print('here2')

        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400

    response['status'] = 'ok'
    response['payload'] = data
    response['message'] = 'Prediction successful. Transactions have been marked.'

    return jsonify(response), 202
