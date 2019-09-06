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
        response.update({'validation': {'status': 'ok', 'message': ''},
                         'date': {'status': 'ok', 'message': ''},
                         'db_dump': {'status': 'ok', 'message': ''}})
        data = request.get_json()
        if not isinstance(data, list):
            [response.pop(key) for key in ['date', 'db_dump', 'validation']]
            raise Exception('data is not a list')
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
            #check dateid if dateid is valid
            try:
                datetime.datetime.strptime(elem['dateid'], '%Y%m%d').date()
            except:
                response['date']['status'] = 'Error in checking datetime, please see line items that are failing'
                response['date']['message'] += (str(index))
        if response['validation']['status'] != 'ok':
            [response.pop(key) for key in ['date', 'db_dump']]
            raise Exception('error with input data')
        if response['date']['status'] != 'ok':
            [response.pop(key) for key in ['db_dump']]
            raise Exception('error in dateid check')
        #Inserting data into fx rates table
        try:
            db.session.bulk_insert_mappings(FXRates, data)
            db.session.commit()
        except exc.SQLAlchemyError as e:
                response['db_dump']['status'] = 'error'
                response['db_dump']['message'] = str(e).split('\n')[0]
                raise Exception('error in db insertion')
        response['status'] = 'OK'
        response['message'] = 'Data successfully validated and inserted to DB'
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'error'
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201
