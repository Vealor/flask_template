'''
Auth Endpoints
'''
import json
import random
import string
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.errors import *
from src.models import *
from src.util import send_mail, validate_request_data, create_log
from src.wrappers import has_permission, exception_wrapper

auth = Blueprint('auth', __name__)
#===============================================================================
# make base lighthouse superuser
# @auth.route('/create_base_lh_superuser', methods=['POST'])
# @exception_wrapper()
# def create_base_lh_superuser():
#     response = { 'status': 'ok', 'message': '', 'payload': [] }
#     has_super = User.query.filter_by(is_superuser=True).first()
#     if has_super:
#         raise InputError("Already Made")
#     db.session.add(User(
#         username = 'lh-admin', password = User.generate_hash('Kpmg1234%'),
#         email = 'ca-fmgvalhrhadmin@kpmg.ca',
#         initials = 'lh'.upper(), first_name = 'Lighthouse', last_name = 'GVA',
#         role = 'tax_master', is_system_administrator = True, is_superuser = True
#     ))
#     db.session.commit()
#     response['message'] = 'Good'
#     return jsonify(response), 201

#===============================================================================
# resets user's password given username and e-mail
# sends email with new temp pass
@auth.route('/reset', methods=['POST'])
@exception_wrapper()
def reset():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    request_types = {
        'username': ['str'],
        'email': ['str'],
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
        create_log(current_user, 'modify', 'User requested password reset', 'E-mail sent')
    db.session.commit()
    response['message'] = 'Password for {} sent to {} if credentials were correct. Check your email for instructions.'.format(data['username'], data['email'])

    return jsonify(response), 201

#===============================================================================
# login
@auth.route('/login', methods=['POST'])
@exception_wrapper()
def login():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    request_types = {
        'username': ['str'],
        'password': ['str'],
    }
    validate_request_data(data, request_types)

    user = User.find_by_username(data['username'])
    if not user or not User.verify_hash(data['password'], user.password):
        raise UnauthorizedError("Wrong Credentials")

    response['access_token'] = create_access_token(identity = data['username'])
    response['refresh_token'] = create_refresh_token(identity = data['username'])
    response['message'] = 'Logged in as {}'.format(data['username'])

    return jsonify(response), 201

#===============================================================================
# refresh access_token with refresh_token
@auth.route('/refresh', methods=['GET'])
@jwt_refresh_token_required
@exception_wrapper()
def refresh():
    user = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['access_token'] = create_access_token(identity = user)
    return jsonify(response), 201

#===============================================================================
# Verify that access_token is valid
@auth.route('/verify', methods=['GET'])
@jwt_required
@exception_wrapper()
def verify_tokens():
    user_identity = get_jwt_identity()
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    return jsonify(response), 200

#===============================================================================
# Get user details (including credentials)
@auth.route('/user_details', methods=['GET'])
@jwt_required
@exception_wrapper()
def get_user_details():
    response = { 'status': 'ok', 'message': '', 'payload': current_user.serialize }
    return jsonify(response), 200

#===============================================================================
# Get user details (including credentials)
@auth.route('/user_details_with_projects', methods=['GET'])
@jwt_required
@exception_wrapper()
def get_user_details_with_projects():
    response = { 'status': 'ok', 'message': '', 'payload': current_user.serialize_user_proj }
    return jsonify(response), 200
