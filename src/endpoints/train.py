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
input_config = json.load(open('src/recovery_identification/input_config.json'))   #Load the configuration info
#===============================================================================
# General
@train.route('/', methods=['POST'])
#@jwt_required
def do_train():
    response = { 'status': '', 'message': '', 'payload': []}
    data = request.get_json()
    if request.method == 'POST':
        print(data)
        response['data'] = data
        # If there are fields missing in the input...
        if not is_input_complete(data):
            response['status'] = "error"
            response['message'] = 'Critical field is not specifed'
            return jsonify(response), 400
        # If the input is not specified correctly...
        if not is_input_correct(data):
            response['status'] = "error"
            response['message'] = 'Input field is incorrect type'
            return jsonify(response), 400
        # Get the date objects. If fail, return an error:
        dates = list(data.keys())
        dates.remove("IS_CLIENT_MODEL")
        #print(dates)
        try:
            check_and_get_date_configuration(data)
        except ValueError as e:
            response['status'] = "error"
            response['message'] = str(e)
            return jsonify(response), 400

        # Check if dates are correctly ordered

    return jsonify(response), 202

# Check that all fields are added to input
def is_input_complete(data):
    required_keys = input_config.keys()
    return all([rk in data.keys() for rk in required_keys])

# RETURNS: bool
# Check that input is the correct type.
def is_input_correct(data):
    dtypes = [input_config[key] for key in data.keys()]
    return all([isinstance(key,eval(typ)) for (key,typ) in zip(data.values(),dtypes)])

# RETURNS: datetime.datetime.date obj
# Dates should be specified as "YYYY-MM-DD"
def get_date_obj_from_str(date_str):
    try:
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return date_obj

# Check if dates are correctly specified so that no overlap occurs
def check_and_get_date_configuration(data):
    train_start = get_date_obj_from_str(data["TRAIN_DATA_START"])
    train_end = get_date_obj_from_str(data["TRAIN_DATA_END"])
    if train_start >= train_end:
        raise ValueError("Invalid Train Data date range.")
    test_start = get_date_obj_from_str(data["TEST_DATA_START"])
    test_end = get_date_obj_from_str(data["TEST_DATA_END"])
    if test_start >= test_end:
        raise ValueError("Invalid Test Data date range.")
    if ((train_start < test_start) and (test_start < train_end)) or ((test_start < train_start) and not (test_end < train_start)):
        raise ValueError("Train and test data ranges overlap.")
    return train_start, train_end, test_start, test_end
