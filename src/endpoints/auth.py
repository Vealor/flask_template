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
# resets user's password given username and e-mail
# sends email with new temp pass
@auth.route('/reset', methods=['POST'])
def reset():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
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

        db.session.commit()
        response['message'] = 'Password for {} sent to {} if credentials were correct. Check your email for instructions.'.format(data['username'], data['email'])
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 201

#===============================================================================
# login
@auth.route('/login', methods=['POST'])
def login():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        request_types = {
            'username': 'str',
            'password': 'str',
        }
        validate_request_data(data, request_types)

        user = User.find_by_username(data['username'])
        if not user or not User.verify_hash(data['password'], user.password):
            response['status'] = 'error'
            response['message'] = 'Wrong Credentials'
            return jsonify(response), 401

        response['access_token'] = create_access_token(identity = data['username'])
        response['refresh_token'] = create_refresh_token(identity = data['username'])
        response['message'] = 'Logged in as {}'.format(data['username'])
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 201

#===============================================================================
# refresh access_token with refresh_token
@auth.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['access_token'] = create_access_token(identity = user)
    return jsonify(response), 201

#===============================================================================
# Verify that access_token is valid
@auth.route('/verify', methods=['GET'])
@jwt_required
def verify_tokens():
    user_identity = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    return jsonify(response), 200

#===============================================================================
# Get user details (including credentials)
@auth.route('/user_details', methods=['GET'])
@jwt_required
def get_user_details():
    response = { 'status': 'ok', 'message': '', 'payload': current_user.serialize }
    return jsonify(response), 200

#===============================================================================
# Get user details (including credentials)
@auth.route('/user_details_with_projects', methods=['GET'])
@jwt_required
def get_user_details_with_projects():
    response = { 'status': 'ok', 'message': '', 'payload': current_user.serialize_user_proj }
    return jsonify(response), 200
