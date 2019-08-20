'''
General Endpoints
'''
import json
import psycopg2
import random
from sqlalchemy import exc
import datetime
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.util import validate_request_data, get_date_obj_from_str
import datetime


fxrates = Blueprint('fxrates', __name__)
#===============================================================================
# General
@fxrates.route('/', methods=['GET'])
def default():
    response = {'status': '', 'message': '', 'payload': [], 'validation' : {'status' : '', 'message' : ''}, 'date' : {'status' : '', 'message' : ''}, 'db_dump' : {'status': '', 'message': ''}}
    data = request.get_json()
    request_types = {
        'dateid': 'str',
        'usdtocad': 'float',
        'cadtousd': 'float',
        'gbptocad': 'float',
        'cadtogbp': 'float'
    }
    for index, elem in enumerate(data):
        try:
            validate_request_data(elem, request_types)
        except:
            response['validation']['status'] = 'Error in validating data, please see line items that are failing'
            response['validation']['message'] += str(index)
            response['status'] = 'error'
            response['message'] = 'error in validation'
        #check dateid if dateid is valid
        try:
            datetime.datetime.strptime(elem['dateid'], '%Y%m%d').date()
        except:
            response['date']['status'] = 'Error in checking datetime, please see line items that are failing'
            response['date']['message'] += (str(index))
            response['status'] = 'error'
            response['message'] = 'error in dateid check'
    if response['validation']['status'] == '':
        response['validation']['status'] = 'OK'
    else:
        return jsonify(response), 400
    if response['date']['status'] == '':
        response['date']['status'] = 'OK'
    else:
        return jsonify(response), 400
    #Inserting data into fx rates table
    try:
        db.session.bulk_insert_mappings(FXRates, data)
        db.session.commit()
        response['db_dump']['status'] = 'OK'
    except exc.SQLAlchemyError as e:
        #FX Rates does not exist
        if 'UndefinedTable' in str(e):
            response['db_dump']['status'] ='error in inserting data to FX Rates table.'
            response['db_dump']['message'] = str(e).split('\n')[0]
            return jsonify(response), 400
        #General error
        else:
            response['db_dump']['status'] = 'general error in inserting to FX Rates table'
            response['db_dump']['message'] = str(e).split('\n')[0]
            return jsonify(response), 400
    response['status'] = 'OK'
    response['message'] = 'Data successfully validated and inserted to DB'
    return jsonify(response), 200


