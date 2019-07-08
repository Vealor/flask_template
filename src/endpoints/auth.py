'''
Auth Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *

auth = Blueprint('auth', __name__)
#===============================================================================
# create admin superuser
@auth.route('/createadminsuperuseraccount', methods=['POST'])
def createadminsuperuseraccount():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()
    if request.method == 'POST':
        for key in ['username', 'password', 'email']:
            if key not in data.keys():
                response['status'] = 'error'
                response['message'] = 'Information improperly supplied.'
                return jsonify(response), 400
        if User.find_by_username(data['username']) or User.superuser_exists():
            response['status'] = 'error'
            response['message'] = 'Username {} already exists or there already is a system superuser.'.format(data['username'])
            return jsonify(response), 400
        elif 'special_token' in data.keys() and data['special_token'] == 'lhsuperamazingawesometoken':
            response['status'] = 'ok'
            new_user = User(
                username = data['username'],
                password = User.generate_hash(data['password']),
                email = data['email'],
                is_superuser = True
            )
            new_user.save_to_db()
            response['access_token'] = create_access_token(identity = data['username'])
            response['refresh_token'] = create_refresh_token(identity = data['username'])
            response['message'] = 'User {} was successfully created.'.format(data['username'])
        else:
            response['status'] = 'error'
            response['message'] = 'Information improperly supplied.'
            return jsonify(response), 400
    return jsonify(response), 201

# registration
@jwt_required
@auth.route('/register', methods=['POST'])
def register():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()
    if request.method == 'POST':
        if [(i) for i in ['username', 'password', 'email'] if key not in data.keys()]:
            response['status'] = 'error'
            response['message'] = 'Information improperly supplied.'
            return jsonify(response), 400
        elif Users.find_by_username(data['username']):
            response['status'] = 'error'
            response['message'] = 'Username {} already exists.'.format(data['username'])
            return jsonify(response), 400
        else:
            response['status'] = 'ok'
            new_user = Users(
                username = data['username'],
                password = Users.generate_hash(data['password']),
                email = data['email']
            )
            new_user.save_to_db()
            response['access_token'] = create_access_token(identity = data['username'])
            response['refresh_token'] = create_refresh_token(identity = data['username'])
            response['message'] = 'User {} was successfully created.'.format(data['username'])
    return jsonify(response), 201

# TODO:
#   Acquire roles and other details like this: https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/tokens_from_complex_objects.py
# login
@auth.route('/login', methods=['POST'])
def login():
    def login_failure(response):
        response['status'] = 'error'
        response['message'] = 'Wrong Credentials'
        return jsonify(response), 401
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()
    if request.method == 'POST':
        if [(i) for i in ['username', 'password'] if i not in data.keys()]:
            response['status'] = 'error'
            response['message'] = 'Information improperly supplied.'
            return jsonify(response), 400
        user = User.find_by_username(data['username'])

        if not user:
            return login_failure(response)
        elif User.verify_hash(data['password'], user.password):
            response['status'] = 'ok'
            response['access_token'] = create_access_token(identity = data['username'])
            response['refresh_token'] = create_refresh_token(identity = data['username'])
            # Store the tokens in our store with a status of not currently revoked.
            # add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
            # add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])
            response['message'] = 'Logged in as {}'.format(data['username'])
        else:
            return login_failure(response)
    return jsonify(response), 201

# refresh access_token with refresh_token
@auth.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['access_token'] = create_access_token(identity = user)
    # add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify(response), 201

# Verify that access_token is valid
@auth.route('/verify', methods=['GET'])
@jwt_required
def get_tokens():
    user_identity = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    return jsonify(response), 200
