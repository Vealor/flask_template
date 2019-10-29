'''
DataMapping Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.wrappers import has_permission, exception_wrapper

data_mappings = Blueprint('data_mappings', __name__)
#===============================================================================
# GET ALL DATA MAPPINGS
@data_mappings.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_data_mappings():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = DataMapping.query
    # Set ORDER
    query = query.order_by('project_id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)