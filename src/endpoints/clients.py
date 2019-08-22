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
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = Client.query

        # ID filter
        if id is not None:
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError('ID {} does not exist.'.format(id))
        # Set ORDER
        query = query.order_by('name')
        # Set LIMIT
        query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
        # Set OFFSET
        query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

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
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'line_of_business_id': 'int'
        }
        validate_request_data(data, request_types)
        # check if this name exists
        check = Client.query.filter_by(name=data['name']).first()
        if check:
            raise ValueError('Client {} already exist.'.format(data['name']))
        # check if this line of business exists
        lineofbusiness = LineOfBusiness.find_by_id(data['line_of_business_id'])
        if not lineofbusiness:
            raise ValueError('Line of Business with ID {} does not exist.'.format(data['line_of_business_id']))

        # INSERT transaction
        client_id = Client(
            name = data['name'],
            client_line_of_business = lineofbusiness
        ).save_to_db()

        response['message'] = 'Created client {}'.format(data['name'])
        response['payload'] = [Client.find_by_id(client_id).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# UPDATE A CLIENT
@clients.route('/<path:id>', methods=['PUT'])
# @jwt_required
def update_client(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'line_of_business_id': 'int'
        }
        validate_request_data(data, request_types)

        # UPDATE transaction
        query = Client.find_by_id(id)
        if not query:
            raise ValueError('Client ID {} does not exist.'.format(id))

        # check if this name exists
        check = Client.query.filter_by(name=data['name']).filter(Client.id != id).first()
        if check:
            raise ValueError('Client name {} already exists.'.format(data['name']))

        # check if this line of business exists
        lineofbusiness = LineOfBusiness.find_by_id(data['line_of_business_id'])
        if not lineofbusiness:
            raise ValueError('Line of Business id does not exist.'.format(data['line_of_business_id']))

        query.name = data['name']
        query.client_line_of_business = lineofbusiness
        query.update_to_db()

        response['message'] = 'Updated client with id {}'.format(id)
        response['payload'] = [Client.find_by_id(id).serialize]
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
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        query = Client.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Client ID {} does not exist.'.format(id))

        # fail delete if has projects, models, or classification_rules
        if query.client_projects.all() or query.client_client_models.all():
        # if query.client_projects.all() or query.client_classification_rules.all() or query.client_client_models.all():
            raise Exception('Client not deleted. Client has active projects, models, or classification rules.')

        client = query.serialize
        query.delete_from_db()

        response['message'] = 'Deleted client id {}'.format(client['id'])
        response['payload'] = [client]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
