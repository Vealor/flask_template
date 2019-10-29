'''
Jurisdiction Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.wrappers import has_permission, exception_wrapper

jurisdictions = Blueprint('jurisdictions', __name__)
#===============================================================================
# GET ALL JURISDICTIONS
@jurisdictions.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def default():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['payload'] = Jurisdiction.list()
    return jsonify(response)
