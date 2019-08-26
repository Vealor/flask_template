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
@fxrates.route('/', methods=['POST'])
def insert_fxrates_data():
    try:
        response = {'status': 'ok', 'message': '', 'payload': []}
        response.update({
      'validation': {'status': 'ok', 'message': ''},
      'date': {'status': 'ok', 'message': ''},
      'db_dump': {'status': 'ok', 'message': ''}
    })
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
                response['message'] = 'error with input data'
            #check dateid if dateid is valid
            try:
                datetime.datetime.strptime(elem['dateid'], '%Y%m%d').date()
            except:
                response['date']['status'] = 'Error in checking datetime, please see line items that are failing'
                response['date']['message'] += (str(index))
                response['status'] = 'error'
                response['message'] = 'error in dateid check'
        if response['validation']['status'] != 'ok':
            return jsonify(response), 400
        if response['date']['status'] != 'ok':
            return jsonify(response), 400
        #Inserting data into fx rates table
        try:
            db.session.bulk_insert_mappings(FXRates, data)
            db.session.commit()
            response['db_dump']['status'] = 'OK'
        except exc.SQLAlchemyError as e:
                response['db_dump']['status'] = 'general error in inserting to FX Rates table'
                response['db_dump']['message'] = str(e).split('\n')[0]
                return jsonify(response), 400
        response['status'] = 'OK'
        response['message'] = 'Data successfully validated and inserted to DB'
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201
