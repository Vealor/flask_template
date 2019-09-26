'''
Transaction Endpoints
'''
import datetime
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

transactions = Blueprint('transactions', __name__)
#===============================================================================
# GET ALL TRANSACTION
@transactions.route('/', defaults={'id':None}, methods=['GET'])
@transactions.route('/<path:id>', methods=['GET'])
# @jwt_required
# @has_permission([])
def get_transactions(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        if id is None:
            raise ValueError('Please specify a Project ID for the transactions query.')

        query = Transaction.query

        # Project ID filter
        query = query.filter_by(project_id=id)
        if not query.first():
            raise ValueError('ID {} does not exist.'.format(id))
        # Set ORDER
        query = query.order_by('id')
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
    return jsonify(response), 200

#===============================================================================
# Check if transaction locked

#===============================================================================
# Lock Transaction

#===============================================================================
# Unlock Transaction

#===============================================================================
# UPDATE A TRANSACTION information
@transactions.route('/<path:id>', methods=['PUT'])
# @jwt_required
# @has_permission([])
def update_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'username': 'str',
            'email': 'str',
            'initials': 'str',
            'first_name': 'str',
            'last_name': 'str',
            'role': 'str' # TODO: if user does not have correct role, do not do this
        }
        validate_request_data(data, request_types)

        # UPDATE user
        query = User.find_by_id(id)
        if not query:
            raise ValueError('User ID {} does not exist.'.format(id))

        # check if data already exists
        check = User.query.filter_by(username=data['username']).filter(User.id != id).first()
        if check:
            raise ValueError('Username {} already exists.'.format(data['username']))
        # check if this email exists
        check = User.query.filter_by(email=data['email']).filter(User.id != id).first()
        if check:
            raise ValueError('User email {} already exists.'.format(data['email']))
        # check if these initials exist
        check = User.query.filter_by(initials=data['initials']).first()
        if check:
            raise ValueError('User initials {} already exist.'.format(data['initials']))

        # update user data
        # query.modified =

        query.username = data['username']
        query.email = data['email']
        query.initials = data['initials'].upper()
        query.first_name = data['first_name']
        query.last_name = data['last_name']
        if data['role'] not in Roles.__members__:
            raise ValueError('Specified role does not exists')
        query.role = data['role']

        db.session.commit()
        response['message'] = 'Updated user with id {}'.format(id)
        response['payload'] = [User.find_by_id(id).serialize]
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 200
