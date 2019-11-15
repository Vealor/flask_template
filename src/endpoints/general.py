'''
General Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.errors import *
from src.models import *
from src.wrappers import has_permission, exception_wrapper

general = Blueprint('general', __name__)
#===============================================================================
# General
@general.route('/', methods=['GET'])
@exception_wrapper()
def default():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['VERSION'] = current_app.config['VERSION']
    response['payload'] = []
    return jsonify(response)
