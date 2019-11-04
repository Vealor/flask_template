'''
Vendor Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data
from src.wrappers import has_permission, exception_wrapper

vendors = Blueprint('vendors', __name__)
#===============================================================================
# GET ALL VENDORS
@vendors.route('/', defaults={'id':None}, methods=['GET'])
@vendors.route('/<path:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
def get_vendors(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = Vendor.query
    # ID filter
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise ValueError('ID {} does not exist.'.format(id))
    # # Set ORDER
    query = query.order_by('name')
    # # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
    # # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)

#===============================================================================
# POST NEW VENDOR
@vendors.route('/', methods=['POST'])
# @jwt_required
@exception_wrapper()
def post_vendor():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # input validation
    request_types = {
        'name': 'str'
    }
    validate_request_data(data, request_types)

    check = Vendor.query.filter_by(name=data['name']).first()
    if check:
        raise ValueError('Vendor {} already exist.'.format(data['name']))

    # INSERT transaction
    vendor_id = Vendor(
        name = data['name']
    ).save_to_db()

    response['message'] = 'Created vendor {}'.format(data['name'])
    response['payload'] = [Vendor.find_by_id(vendor_id).serialize]

    return jsonify(response), 201

#===============================================================================
# UPDATE A VENDOR
@vendors.route('/<path:id>', methods=['PUT'])
# @jwt_required
@exception_wrapper()
def update_vendor(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # input validation
    request_types = {
        'name': 'str'
    }
    validate_request_data(data, request_types)

    # UPDATE transaction
    query = Vendor.query.filter_by(id=id).first()
    if not query:
        raise ValueError('Vendor ID {} does not exist.'.format(id))

    query.name = data['name']
    query.update_to_db()

    response['message'] = 'Updated vendor with id {}'.format(data['id'])
    response['payload'] = [Vendor.find_by_id(data['id']).serialize]

    return jsonify(response)

#===============================================================================
# DELETE A VENDOR
@vendors.route('/<path:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
def delete_vendor(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = Vendor.query.filter_by(id=id).first()
    if not query:
        raise ValueError('Vendor ID {} does not exist.'.format(id))
    vendor = query.serialize
    query.delete_from_db()

    response['message'] = 'Deleted vendor id {}'.format(vendor['id'])
    response['payload'] = [vendor]

    return jsonify(response)
