'''
Auth Endpoints
'''
import json
import random
import string
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.models import *
from src.util import send_mail, validate_request_data

auth = Blueprint('auth', __name__)

#===============================================================================
# create admin superuser
@auth.route('/createadminsuperuseraccount', methods=['POST'])
def createadminsuperuseraccount():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    if request.method == 'POST':
        request_types = {
            'username': 'str',
            'password': 'str',
            'email': 'str',
            'first_name': 'str',
            'last_name': 'str',
            'special_token': 'str',
            'role': 'str',
            'initials': 'str'
        }
        try:
            validate_request_data(data, request_types)
        except ValueError as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return jsonify(response), 400

        if User.find_by_username(data['username']) or User.superuser_exists():
            response['status'] = 'error'
            response['message'] = 'Username {} already exists or there already is a system superuser.'.format(data['username'])
            return jsonify(response), 400

        if data['special_token'] != 'lhsuperamazingawesometoken':
            response['status'] = 'error'
            response['message'] = 'Information improperly supplied.'
            return jsonify(response), 400

        response['status'] = 'ok'
        new_user = User(
            username = data['username'],
            password = User.generate_hash(data['password']),
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name'],
            is_superuser = True,
            role = data['role'],
            initials = data['initials']
        )
        new_user.save_to_db()
        response['access_token'] = create_access_token(identity = data['username'])
        response['refresh_token'] = create_refresh_token(identity = data['username'])
        response['message'] = 'User {} was successfully created.'.format(data['username'])

    return jsonify(response), 201

#===============================================================================
# resets user's password given username and e-mail
# sends email with new temp pass
@auth.route('/reset', methods=['POST'])
def reset():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        request_types = {
            'username': 'str',
            'email': 'str',
        }
        validate_request_data(data, request_types)

        user = User.find_by_username(data['username'])
        if user and user.email == data['email']:
            lettersAndDigits = string.ascii_letters + string.digits
            newpass = ''.join(random.choice(lettersAndDigits) for i in range(10))
            passhash = User.generate_hash(newpass)

            user.req_pass_reset = True
            user.password = passhash

            mailbody = '''
            <h2>Password reset information</h2>
            <strong>username: </strong>'''+data['username']+'''<br>
            <strong>new pass: </strong>'''+newpass+'''
            '''
            send_mail(data['email'], 'Password Reset', mailbody)

            user.update_to_db()

        response['status'] = 'ok'
        response['message'] = 'Password for {} sent to {} if credentials were correct. Check your email for instructions.'.format(data['username'], data['email'])
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# TODO:
#   Acquire roles and other details like this: https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/tokens_from_complex_objects.py
# login
@auth.route('/login', methods=['POST'])
def login():
    response = { 'status': '', 'message': '', 'payload': [] }
    data = request.get_json()

    print(data)

    try:
        request_types = {
            'username': 'str',
            'password': 'str',
        }
        validate_request_data(data, request_types)
        print('made it1')

        try:
            user = User.find_by_username(data['username'])
        except Exception as e:
            print(e)
        print('made it2')
        if not user or not User.verify_hash(data['password'], user.password):
            response['status'] = 'error'
            response['message'] = 'Wrong Credentials'
            return jsonify(response), 401
            print('made it3')

        print('made it4')
        response['status'] = 'ok'
        response['access_token'] = create_access_token(identity = data['username'])
        response['refresh_token'] = create_refresh_token(identity = data['username'])
        response['message'] = 'Logged in as {}'.format(data['username'])
        response['payload'] = []
    except Exception as e:
        print("BAD")
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 201

#===============================================================================
# refresh access_token with refresh_token
@auth.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['access_token'] = create_access_token(identity = user)
    # add_token_to_database(access_token, app.config['JWT_IDENTITY_CLAIM'])
    return jsonify(response), 201

#===============================================================================
# Verify that access_token is valid
@auth.route('/verify', methods=['GET'])
@jwt_required
def get_tokens():
    user_identity = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    return jsonify(response), 200

#===============================================================================
# Get user details (including credentials)
@auth.route('/user_details', methods=['GET'])
@jwt_required
def get_user_details():
    user = current_user
    response = { 'status': 'ok', 'message': '', 'payload': user.serialize }
    return jsonify(response), 200
