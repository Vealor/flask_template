'''
Role Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *

roles = Blueprint('roles', __name__)
#===============================================================================
# GET ALL LineOfBusinessSectors
@roles.route('/', methods=['GET'])
# @jwt_required
def get_roles():
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        response['message'] = ''
        response['payload'] = Roles.list()
    except ValueError as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 500
    return jsonify(response)
