'''
Client Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

clients = Blueprint('clients', __name__)
#===============================================================================
# GET ALL CLIENT
@clients.route('/', defaults={'id':None}, methods=['GET'])
@clients.route('/<path:id>', methods=['GET'])
# @jwt_required
def get_clients(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = Client.query

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
# POST NEW CLIENT
@clients.route('/', methods=['POST'])
# @jwt_required
def post_client():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'industry_id': 'int'
        }
        validate_request_data(data, request_types)

        query = Client.query.filter_by(name=data['name']).first()
        if query:
            raise ValueError('Client "{}" already exist.'.format(data['name']))

        # INSERT transaction
        Client(
            name = data['name'],
            industry_id = data['industry_id']
        ).save_to_db()

        response['status'] = 'ok'
        response['message'] = 'Created client {}'.format(data['name'])
        response['payload'] = [Client.find_by_name(data['name']).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# UPDATE A CLIENT
@clients.route('/<path:id>', methods=['UPDATE'])
# @jwt_required
def update_client(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'industry_id': 'int'
        }
        validate_request_data(data, request_types)

        # UPDATE transaction
        query = Client.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Client ID {} does not exist.'.format(id))

        query.name = data['name']
        query.industry_id = data['industry_id']
        query.update_to_db()

        response['status'] = 'ok'
        response['message'] = 'Updated client with id {}'.format(data['id'])
        response['payload'] = [Client.find_by_id(data['id']).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# DELETE A CLIENT
@clients.route('/<path:id>', methods=['DELETE'])
# @jwt_required
def delete_client(id):
    response = { 'status': '', 'message': '', 'payload': [] }

    try:
        query = Client.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Client ID {} does not exist.'.format(id))
        client = query.serialize
        query.delete_from_db()

        response['status'] = 'ok'
        response['message'] = 'Deleted client id {}'.format(client['id'])
        response['payload'] = [client]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400

    return jsonify(response)
