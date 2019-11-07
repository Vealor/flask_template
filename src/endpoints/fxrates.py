'''
General Endpoints
'''
import json
import random
import datetime
import json
import requests
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import desc, exc
from src.models import *
from src.util import *
from src.wrappers import has_permission, exception_wrapper

fxrates = Blueprint('fxrates', __name__)
#===============================================================================
# GET AND UPDATE FXRATES
@fxrates.route('/', methods=['GET'])
@exception_wrapper()
def get_fxrates():
    response = {'status': 'ok', 'message': '', 'payload': []}

    query = FXRates.query.order_by(desc(FXRates.date)).first().serialize

    if query['date'] < datetime.datetime.now().date():
        params = {'start_date' : str(query['date']), 'end_date' : str(datetime.datetime.now().date())}
        results = requests.get('http://bankofcanada.ca/valet/observations/FXCADUSD', params=params).json()
        database_insert = [{'date': dict['d'], 'usdtocad': dict['FXCADUSD']['v']} for dict in results['observations'] if dict['d'] > str(query['date'])]
        db.session.bulk_insert_mappings(FXRates, database_insert)
        db.session.commit()
    response['payload'] = [i.serialize for i in FXRates.query.order_by(desc(FXRates.date)).all()]

    return jsonify(response), 201
