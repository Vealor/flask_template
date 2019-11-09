'''
Role Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.errors import *
from src.models import *
from src.wrappers import has_permission, exception_wrapper

roles = Blueprint('roles', __name__)
#===============================================================================
# GET ALL Roles
@roles.route('/', methods=['GET'])
# @jwt_required
@exception_wrapper()
def get_roles():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['payload'] = Roles.list()
    return jsonify(response)
