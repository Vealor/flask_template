'''
Predict Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.util import get_date_obj_from_str, validate_request_data

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
                query = ClientModel.query.filter_by(id=data['CLIENT_ID'])
            else:
                query =  MasterModel.query
            query = query.filter_by(status=Activity.pending.value)
            if len(query.all()) != 1:
                raise ValueError("ERROR: Please specify one active model to be used for prediction.")

        except ValueError as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400



    response['status'] = 'ok'
    response['payload'] = str([i.serialize for i in query.all()])
    response['message'] = 'Prediction successful. Transactions have been marked.'

    return jsonify(response), 202
