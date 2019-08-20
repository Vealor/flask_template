'''
Jurisdiction Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *

jurisdictions = Blueprint('jurisdictions', __name__)
#===============================================================================
# GET ALL JURISDICTIONS
@jurisdictions.route('/', methods=['GET'])
# @jwt_required
def default():
    response = { 'status': '', 'message': '', 'payload': [] }

    try:
        response['status'] = 'ok'
        response['message'] = ''
        response['payload'] = Jurisdiction.list()
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
