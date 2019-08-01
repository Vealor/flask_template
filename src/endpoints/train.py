'''
Train Endpoints
'''
import datetime
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import *
from src.util import get_date_obj_from_str, validate_request_data


train = Blueprint('train', __name__)

# ==============================================================================
# Specify the datatypes for the inputs to the train functionality


# ==============================================================================
# General
@train.route('/', methods=['POST'])
# @jwt_required
def do_train():
    response = {'status': '', 'message': '', 'payload': []}
    data = request.get_json()

    if request.method == 'POST':
        request_types = {
            'MODEL_TYPE': 'str',
            'CLIENT_ID': 'int',
            'TRAIN_DATA_START_DATE': 'str',
            'TRAIN_DATA_END_DATE': 'str',
            'TEST_DATA_START_DATE': 'str',
            'TEST_DATA_END_DATE': 'str'
            }
        try:
            # validate input
            validate_request_data(data, request_types)

            # check model type
            if data['MODEL_TYPE'] not in ['client', 'master']:
                raise ValueError('Specified model type `{}` is invalid'.format(data['MODEL_TYPE']))

            # validate date ranges
            train_start = get_date_obj_from_str(data['TRAIN_DATA_START_DATE'])
            train_end = get_date_obj_from_str(data['TRAIN_DATA_END_DATE'])
            test_start = get_date_obj_from_str(data['TEST_DATA_START_DATE'])
            test_end = get_date_obj_from_str(data['TEST_DATA_END_DATE'])
            if train_start >= train_end:
                raise ValueError('Invalid Train Data date range.')
            if test_start >= test_end:
                raise ValueError('Invalid Test Data date range.')
            if not (train_end < test_start or test_end < train_start):
                raise ValueError('Train and test data ranges overlap.')

            # At this point, all database independent checks have been perfrm'd
            # Now, database dependent checks begin
            if data['MODEL_TYPE'] == 'client':
                # Is the client id in the DATABASE?
                if not Client.find_by_id(data['CLIENT_ID']):
                    raise ValueError('Client id \'{}\' is not in the database.'.format(data['CLIENT_ID']))
                # Check if any projects exist for the client
                client_projects = [p.id for p in Project.query.filter_by(client_id = data['CLIENT_ID']).distinct()]
                if len(client_projects) == 0:
                    raise ValueError('Client id \'{}\' has no projects in the database.'.format(data['CLIENT_ID']))
                # Get transactions
                transactions_count = Transaction.query.filter(Transaction.project_id.in_(client_projects)).count()
                if transactions_count < 6000:
                    raise Exception('Not enough data to train a client model.')
            else:
                if Transaction.query.count() < 10000:
                    raise Exception('Not enough data to train a master model.')


        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400


        # Now that all the database checks have been completed, we can submit
        # our request to the compute server
        response['message'] = 'Input is valid. Request submitted to training server.'
        response['payload'] = data
        response['status'] = 'ok'
        return jsonify(response), 202
