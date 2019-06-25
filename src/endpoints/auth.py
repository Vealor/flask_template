'''
Auth Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import UserModel, BlacklistTokenModel

auth = Blueprint('auth', __name__)
#===============================================================================
# registration
@auth.route('/register', methods=['POST'])
def register():
    response = { 'status': '', 'message': '', 'payload': [] }
    print(request.get_data())
    data = request.get_json()
    print(data)
    if request.method == 'POST':
        if UserModel.find_by_username(data['username']):
            response['status'] = 'error'
            response['message'] = 'Username {} already exists.'.format(data['username'])
        else:
            response['status'] = 'ok'
            new_user = UserModel(
                username = data['username'],
                password = UserModel.generate_hash(data['password'])
            )
            new_user.save_to_db()
            response['access_token'] = create_access_token(identity = data['username'])
            response['refresh_token'] = create_refresh_token(identity = data['username'])
            response['message'] = 'User {} was successfully created.'.format(data['username'])
    return jsonify(response)

# TODO:
#   Acquire roles and other details like this: https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/tokens_from_complex_objects.py
@auth.route('/login', methods=['POST'])
def login():
    def login_failure(response):
        response['status'] = 'error'
        response['message'] = 'Wrong Credentials'
        return jsonify(response), 401
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()
    if request.method == 'POST':
        print(data['username'])
        user = UserModel.find_by_username(data['username'])

        if not user:
            print("fail no exist")
            return login_failure(response)
        elif UserModel.verify_hash(data['password'], user.password):
            print('verifying hash')
            response['status'] = 'ok'
            response['access_token'] = create_access_token(identity = data['username'])
            response['refresh_token'] = create_refresh_token(identity = data['username'])
            # Store the tokens in our store with a status of not currently revoked.
            # add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
            # add_token_to_database(refresh_token, app.config['JWT_IDENTITY_CLAIM'])
            response['message'] = 'Logged in as {}'.format(data['username'])
        else:
            print('bad password')
            return login_failure(response)
    print(response)
    return jsonify(response)


@auth.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['access_token'] = create_access_token(identity = user)
    print(response)
    # add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify(response), 201

# Provide a way for a user to look at their tokens
@auth.route('/verify', methods=['GET'])
@jwt_required
def get_tokens():
    user_identity = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    return jsonify(response)
