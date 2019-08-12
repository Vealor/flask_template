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
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    if request.method == 'POST':

        # data type dictionary
        request_types = {
            'MODEL_TYPE': 'str',
            'CLIENT_ID': 'int',
            'TRANSACTION_IDS': 'list'   # A list of integer ids corresponding to the transactions that need prediciton
            }

        # validate input
        try:
            # Do some checks on the input itself.
            validate_request_data(data, request_types)

            if data['MODEL_TYPE'] not in ['client','master']:
                raise ValueError("ERROR: Invalid model type. Must be 'client' or 'master'.")

            if not all([isinstance(id,int) for id in data['TRANSACTION_IDS']]):
                raise ValueError("ERROR: All transaction ids must be integers.")

            if len(data['TRANSACTION_IDS']) == 0:
                raise ValueError("ERROR: Specify at least one transaction to be predicted.")

            # Check the database to see if there are issues.
            if data['MODEL_TYPE'] == 'client':
                active_model = ClientModel.find_active_for_client(data['CLIENT_ID'])
                lh_model = client_model.ClientPredictionModel(active_model.pickle)
            else:
                active_model = MasterModel.find_active()
                lh_model = master_model.MasterPredictionModel(active_model.pickle)
            predictors = active_model.hyper_p['predictors']

            # Get the data to predict
            client_projects = [p.id for p in \
                Project.query.filter_by(client_id = data['CLIENT_ID']).distinct()]
            prediction_transactions = Transaction.query.filter(Transaction.project_id.in_(client_projects))
            entries = [entry.serialize['data'] for entry in prediction_transactions.filter_by(is_approved=False).all()]
            df_predict = pd.read_json('[' + ','.join(entries) + ']',orient='records')
            df_predict = preprocessing_predict(df_predict, predictors)
            #classes = lh_model.predict(df_predict, predictors)
            #print(lh_model.predict_probabilities(df_predict, predictors))
            classes = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]
            classes = {int(key):float(val) for (key,val) in zip(range(0,len(classes)),classes)}

        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400

    response['status'] = 'ok'
    response['payload'] = {'classes': classes}
    response['message'] = 'Prediction successful. Transactions have been marked.'

    return jsonify(response), 202
