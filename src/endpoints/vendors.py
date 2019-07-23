'''
Vendor Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

vendors = Blueprint('vendors', __name__)
#===============================================================================
# GET ALL VENDORS
@vendors.route('/', defaults={'id':None}, methods=['GET'])
@vendors.route('/<path:id>', methods=['GET'])
# @jwt_required
def get_vendors(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = Vendor.query

        # ID filter
        query = query.filter_by(id=id) if id is not None else query
        # Set ORDER
        query = query.order_by('name')
        # Set LIMIT
        query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
        # Set OFFSET
        query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

        response['status'] = 'ok'
        response['message'] = ''
        response['payload'] = [i.serialize for i in query.all()]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# POST NEW VENDOR
@vendors.route('/', methods=['POST'])
# @jwt_required
def post_vendor():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str'
        }
        validate_request_data(data, request_types)

        query = Vendor.query.filter_by(name=data['name']).first()
        if query:
            raise ValueError('Vendor "{}" already exist.'.format(data['name']))

        # INSERT transaction
        Vendor(
            name = data['name']
        ).save_to_db()

        response['status'] = 'ok'
        response['message'] = 'Created vendor {}'.format(data['name'])
        response['payload'] = [Vendor.find_by_name(data['name']).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# UPDATE A VENDOR
@vendors.route('/<path:id>', methods=['UPDATE'])
# @jwt_required
def update_vendor(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
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

        response['status'] = 'ok'
        response['message'] = 'Updated vendor with id {}'.format(data['id'])
        response['payload'] = [Vendor.find_by_id(data['id']).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# DELETE A VENDOR
@vendors.route('/<path:id>', methods=['DELETE'])
# @jwt_required
def delete_vendor(id):
    response = { 'status': '', 'message': '', 'payload': [] }

    try:
        query = Vendor.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Vendor ID {} does not exist.'.format(id))
        vendor = query.serialize
        query.delete_from_db()

        response['status'] = 'ok'
        response['message'] = 'Deleted vendor id {}'.format(vendor['id'])
        response['payload'] = [vendor]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400

    return jsonify(response)
