'''
General Endpoints
'''
import json
import random
from sqlalchemy import exc
import datetime
import json
import requests
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.util import *
from sqlalchemy import desc

fxrates = Blueprint('fxrates', __name__)
#===============================================================================
# General
@fxrates.route('/', methods=['GET'])
def insert_fxrates_data():
    try:
        response = {'status': 'ok', 'message': '', 'payload': []}
        query = FXRates.query.order_by(desc(FXRates.date_id)).first().serialize
        #need assistance on timezones
        if query['date_id'] < datetime.datetime.now().date():
            params = {'start_date' : str(query['date_id']), 'end_date' : str(datetime.datetime.now().date())}
            results = requests.get('http://bankofcanada.ca/valet/observations/FXCADUSD', params=params).json()
            database_insert = [{'date_id': dict['d'], 'usdtocad': dict['FXCADUSD']['v']} for dict in results['observations'] if dict['d'] > str(query['date_id'])]
            db.session.bulk_insert_mappings(FXRates, database_insert)
            db.session.commit()
        response['payload'] = [i.serialize for i in FXRates.query.order_by(desc(FXRates.date_id)).all()]
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'error'
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201
