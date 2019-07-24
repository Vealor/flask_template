'''
Train Endpoints
'''
import datetime
import json
import random
from config import DevelopmentConfig
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
            'CLIENT_ID': 'int',     #If MODEL_TYPE == 'master', assert equal to -1
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

        except ValueError as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400

        # At this point, all database independent checks have been perfrm'd
        # Now, database dependent checks begin (TO BE COMPLETED LATER)

        # Now that all the database checks have been completed, we can submit
        # our request to the compute server
        response['message'] = 'Input is valid. Request submitted to training server.'
        response['payload'] = data
        response['status'] = 'ok'
        return jsonify(response), 202
