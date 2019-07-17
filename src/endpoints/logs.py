'''
Log Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *

logs = Blueprint('logs', __name__)
#===============================================================================
# GET ALL LOGS
@logs.route('/', methods=['GET'])
# @jwt_required
# PERMISSION IT ADMIN
def default():
    response = { 'status': '', 'message': '', 'payload': ['potato'] }
    args = request.args.to_dict()

    try:
        limit = int(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else 10000
        offset = int(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else 0

        response['status'] = 'ok'
        response['message'] = 'Got first '+str(limit)+' logs.'
        response['payload'] = [i.serialize for i in Log.query.order_by('timestamp').limit(limit).offset(offset).all()]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = e
        response['payload'] = []
    return jsonify(response)
