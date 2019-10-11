'''
Jurisdiction Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.jwt_helpers import has_permission
from src.models import *

jurisdictions = Blueprint('jurisdictions', __name__)
#===============================================================================
# GET ALL JURISDICTIONS
@jurisdictions.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
def default():
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        response['payload'] = Jurisdiction.list()
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response)
