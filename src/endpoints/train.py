'''
Train Endpoints
'''
import datetime
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import *
from src.recovery_identification import *

train = Blueprint('train', __name__)

input_config = json.load(open('src/recovery_identification/input_config.json'))
# ==============================================================================
# General
@train.route('/', methods=['POST'])
# @jwt_required
def do_train():
    response = {'status': '', 'message': '', 'payload': []}
    data = request.get_json()
    if request.method == 'POST':
        response['data'] = data

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

        # Check 3: Get the date objects. If fail, return an error:
        dates = list(data.keys())
        dates.remove("IS_CLIENT_MODEL")
        try:
            train_start = get_date_obj_from_str(data["TRAIN_DATA_START"])
            train_end = get_date_obj_from_str(data["TRAIN_DATA_END"])
            if train_start >= train_end:
                raise ValueError("Invalid Train Data date range.")
            test_start = get_date_obj_from_str(data["TEST_DATA_START"])
            test_end = get_date_obj_from_str(data["TEST_DATA_END"])
            if test_start >= test_end:
                raise ValueError("Invalid Test Data date range.")
            if ((train_start < test_start) and (test_start < train_end)) or \
                    ((test_start < train_start) and not (test_end < train_start)):
                raise ValueError("Train and test data ranges overlap.")
        except ValueError as e:
            response['status'] = "error"
            response['message'] = str(e)
            return jsonify(response), 400

        # Check if dates are correctly ordered

    return jsonify(response), 202


# ====== HELPERS ================================ ##
# RETURNS: datetime.datetime.date obj
# Dates should be specified as "YYYY-MM-DD"
def get_date_obj_from_str(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return date_obj
