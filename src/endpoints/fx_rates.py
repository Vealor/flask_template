'''
General Endpoints
'''
import datetime
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from src.models import db, FXRate
from src.wrappers import has_permission, exception_wrapper

fx_rates = Blueprint('fx_rates', __name__)
#===============================================================================
# GET AND UPDATE FXRATES
@fx_rates.route('/', methods=['GET'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_fx_rates():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    last_date = FXRate.query.order_by(desc(FXRate.date)).first()
    last_date = last_date.get_dates if last_date else last_date

    if not last_date or last_date['datetime'] < datetime.datetime.now().date():
        results = requests.get('http://bankofcanada.ca/valet/observations/FXCADUSD').json()
        if not last_date:
            database_insert = [{'date': dict['d'], 'usdtocad': dict['FXCADUSD']['v']} for dict in results['observations']]
        else:
            database_insert = [{'date': dict['d'], 'usdtocad': dict['FXCADUSD']['v']} for dict in results['observations'] if dict['d'] > str(last_date['datetime'])]
        db.session.bulk_insert_mappings(FXRate, database_insert)
        db.session.commit()

    query = FXRate.query
    query = query.order_by(desc('date'))
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)
    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 201
