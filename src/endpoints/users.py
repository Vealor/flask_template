'''
User Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

users = Blueprint('users', __name__)
#===============================================================================
# GET ALL USER
@users.route('/', defaults={'id':None}, methods=['GET'])
@users.route('/<path:id>', methods=['GET'])
# @jwt_required
def get_users(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = User.query

        # ID filter
        if id is not None:
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError('ID {} does not exist.'.format(id))
        # Set ORDER
        query = query.order_by('username')
        # Set LIMIT
        query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
        # Set OFFSET
        query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

        response['message'] = ''
        response['payload'] = [i.serialize_proj for i in query.all()] if 'projects' in args.keys() else [i.serialize for i in query.all()]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)

#===============================================================================
# POST NEW USER
@users.route('/', methods=['POST'])
# @jwt_required
def post_user():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'username': 'str',
            'password': 'str',
            'email': 'str',
            'initials': 'str',
            'first_name': 'str',
            'last_name': 'str',
            'role': 'str'
        }
        validate_request_data(data, request_types)
        # check if this username exists
        check = User.query.filter_by(username=data['username']).first()
        if check:
            raise ValueError('Username {} already exists.'.format(data['username']))
        # check if this email exists
        check = User.query.filter_by(email=data['email']).first()
        if check:
            raise ValueError('User email {} already exists.'.format(data['email']))

        # ENUM check
        if data['role'] not in Roles.__members__:
            raise ValueError('Specified role does not exists')

        # INSERT user
        new_user = User(
            username = data['username'],
            password = User.generate_hash(data['password']),
            email = data['email'],
            initials = data['initials'].upper(),
            first_name = data['first_name'],
            last_name = data['last_name'],
            role = data['role']
        )
        db.session.add(new_user)
        db.session.flush()

        db.session.commit()
        response['message'] = 'Created user {}'.format(data['username'])
        response['payload'] = [User.find_by_id(new_user.id).serialize]
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# UPDATE A USER information
@users.route('/<path:id>', methods=['PUT'])
# @jwt_required
def update_user(id):
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
        check = User.query.filter_by(email=data['email']).filter(User.id != id).first()
        if check:
            raise ValueError('User email {} already exists.'.format(data['email']))

        # update user data
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
    return jsonify(response)

#===============================================================================
# Check A USER password
@users.route('/<path:id>/passcheck', methods=['POST'])
# @jwt_required
def check_password(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'password': 'str'
        }
        validate_request_data(data, request_types)

        query = User.find_by_id(id)
        if not User.verify_hash(data['password'], query.password):
            response['status'] = 'error'
            response['message'] = 'Password Invalid'
            return jsonify(response), 401

        response['message'] = 'Password Valid'
        response['payload'] = []
    except ValueError as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 200

#===============================================================================
# UPDATE A USER password
@users.route('/<path:id>/passchange', methods=['PUT'])
# @jwt_required
def update_user_password(id):
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'password': 'str',
            'newpassword': 'str',
        }
        validate_request_data(data, request_types)

        query = User.find_by_id(id)
        if not User.verify_hash(data['password'], query.password):
            response['status'] = 'error'
            response['message'] = 'Password Invalid'
            return jsonify(response), 401

        query.password = User.generate_hash(data['newpassword'])
        query.req_pass_reset = False

        db.session.commit()
        response['status'] = 'ok'
        response['message'] = 'Password changed'
        response['payload'] = []
    except ValueError as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# DELETE A USER
@users.route('/<path:id>', methods=['DELETE'])
# @jwt_required
def delete_user(id):
    response = { 'status': '', 'message': '', 'payload': [] }

    try:
        query = User.query.filter_by(id=id).first()
        if not query:
            raise ValueError('User ID {} does not exist.'.format(id))

        user = query.serialize
        db.session.delete(query)

        db.session.commit()
        response['status'] = 'ok'
        response['message'] = 'Deleted user id {}'.format(user['id'])
        response['payload'] = [user]
    except Exception as e:
        db.session.rollback()
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
