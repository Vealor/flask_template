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
from sqlalchemy import create_engine
from src.util import get_date_obj_from_str


train = Blueprint('train', __name__)

# ==============================================================================
# Specify the datatypes for the inputs to the train functionality
input_config = {
    "MODEL_TYPE": "str",
    "MODEL_NAME": "str",
    "MODEL_ID": "int",
    "TRAIN_DATA_START_DATE": "str",
    "TRAIN_DATA_END_DATE": "str",
    "TEST_DATA_START_DATE": "str",
    "TEST_DATA_END_DATE": "str"
    }

# ==============================================================================
# General
@train.route('/', methods=['POST'])
# @jwt_required
def do_train():
    response = {'status': '', 'message': '', 'payload': []}
    data = request.get_json()
    if request.method == 'POST':
        #response['data'] = data

        # Check 1: Check if fields are missing in the input.
        required_keys = input_config.keys()
        is_input_complete = all([rk in data.keys() for rk in required_keys])
        if not is_input_complete:
            response['status'] = "error"
            response['message'] = 'Critical field is not specifed'
            return jsonify(response), 400

        # Check 2: Check if the input has the correct datatypes.
        dtypes = [input_config[key] for key in data.keys()]
        is_input_correct = all([isinstance(key, eval(typ)) for (key, typ) in
                zip(data.values(), dtypes)])
        if not is_input_correct:
            response['status'] = "error"
            response['message'] = 'Input field is incorrect type'
            return jsonify(response), 400

        # Check 3: Check that model type is valid;
        model_type = data["MODEL_TYPE"]
        if model_type not in ["client", "industry"]:
            response['status'] = "error"
            response['message'] = 'Specified model type `{}` is invalid'.format(model_type)
            return jsonify(response), 400

        # Check 4: Get the date objects. If fail, return an error:
        try:
            train_start = get_date_obj_from_str(data["TRAIN_DATA_START_DATE"])
            train_end = get_date_obj_from_str(data["TRAIN_DATA_END_DATE"])
            if train_start >= train_end:
                raise ValueError("Invalid Train Data date range.")
            test_start = get_date_obj_from_str(data["TEST_DATA_START_DATE"])
            test_end = get_date_obj_from_str(data["TEST_DATA_END_DATE"])
            if test_start >= test_end:
                raise ValueError("Invalid Test Data date range.")
            if ((train_start < test_start) and (test_start < train_end)) or \
                    ((test_start < train_start) and not (test_end < train_start)):
                raise ValueError("Train and test data ranges overlap.")
        except ValueError as e:
            response['status'] = "error"
            response['message'] = str(e)
            return jsonify(response), 400

        # At this point, all database independent checks have been perfrm'd
        # Now, database dependent checks begin (TO BE COMPLETED LATER)

        # Now that all the database checks have been completed, we can submit
        # our request to the compute server
        response['message'] = "Input is valid. Request submitted to training server."
        response['payload'] = data
        response['status'] = 'ok'
        return jsonify(response), 202
