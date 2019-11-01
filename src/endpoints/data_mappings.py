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
    if 'caps_gen_id' not in args.keys():
        raise ValueError('Please specify a caps_gen_id ID as an argument for the data_mappings query.')
    query = query.filter_by(caps_gen_id=args['caps_gen_id'])

    # Set ORDER
    query = query.order_by('caps_gen_id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)

#===============================================================================
# CREATE NEW DATA MAPPING

# not done as new mappings can't be created
# they are made during the CAPSGen process in /caps_gen/init

#===============================================================================
# UPDATE DATA MAPPING
@data_mappings.route('/<int:id>', methods=['PUT'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def update_data_mapping(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    request_types = {
    }
    validate_request_data(data, request_types)

    # UPDATE data mapping
    query = DataMapping.find_by_id(id)
    if not query:
        raise ValueError('User ID {} does not exist.'.format(id))

    query.column_name = data['column_name']

    db.session.commit()
    response['message'] = 'Updated data_mapping with id {}'.format(id)
    response['payload'] = [DataMapping.find_by_id(id).serialize]

    return jsonify(response)
