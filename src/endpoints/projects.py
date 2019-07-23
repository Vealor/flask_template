'''
Project Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

projects = Blueprint('projects', __name__)
#===============================================================================
# GET ALL CLIENT
@projects.route('/', defaults={'id':None}, methods=['GET'])
@projects.route('/<path:id>', methods=['GET'])
# @jwt_required
def get_projects(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = Project.query

        # ID filter
        query = query.filter_by(id=id) if id is not None else query
        # Set ORDER
        query = query.order_by('name')
        # Query on is_approved (is_approved, 1 or 0)
        query = query.filter_by(is_approved=bool(args['is_approved'])) if 'is_approved' in args.keys() and args['is_approved'].isdigit() else query
        # Query on is_archived (is_archived, 1 or 0)
        query = query.filter_by(is_archived=bool(args['is_archived'])) if 'is_archived' in args.keys() and args['is_archived'].isdigit() else query
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
@projects.route('/', methods=['POST'])
# @jwt_required
def post_project():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'client_id': 'int'
        }
        validate_request_data(data, request_types)
        # check if this name exists
        query = Project.query.filter_by(name=data['name']).first()
        if query:
            raise ValueError('Project "{}" already exist.'.format(data['name']))
        # check if this client exists
        query = Client.query.filter_by(id=data['client_id']).first()
        if not query:
            raise ValueError('Client id does not exist.'.format(data['client_id']))

        # INSERT transaction
        Project(
            name = data['name'],
            client_id = data['client_id']
        ).save_to_db()

        response['status'] = 'ok'
        response['message'] = 'Created project {}'.format(data['name'])
        response['payload'] = [Project.find_by_name(data['name']).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# UPDATE A CLIENT
@projects.route('/<path:id>', methods=['UPDATE'])
# @jwt_required
def update_project(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'is_approved': 'bool',
            'is_archived': 'bool'
        }
        validate_request_data(data, request_types)

        # UPDATE transaction
        query = Project.query.find_by_id(id)
        if not query:
            raise ValueError('Project ID {} does not exist.'.format(id))

        # check if this name exists
        check = Project.query.filter_by(name=data['name']).filter(Project.id != id).first()
        if check:
            raise ValueError('Project name < {} > already exist.'.format(data['name']))

        query.name = data['name']
        query.is_approved = data['is_approved']
        query.is_archived = data['is_archived']
        query.update_to_db()

        response['status'] = 'ok'
        response['message'] = 'Updated project with id {}'.format(id)
        response['payload'] = [Project.find_by_id(id).serialize]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# DELETE A CLIENT
@projects.route('/<path:id>', methods=['DELETE'])
# @jwt_required
def delete_project(id):
    response = { 'status': '', 'message': '', 'payload': [] }

    try:
        query = Project.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Project ID {} does not exist.'.format(id))

        project = query.serialize
        query.delete_from_db()

        response['status'] = 'ok'
        response['message'] = 'Deleted project id {}'.format(project['id'])
        response['payload'] = [project]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
