'''
Area Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *

areas = Blueprint('areas', __name__)
#===============================================================================
# GET ALL LINEOFBUSINESS
@areas.route('/', methods=['GET'])
# @jwt_required
def default():
    response = { 'status': 'ok', 'message': '', 'payload': ['AREAS TBD'] }

    try:
        # query = LineOfBusiness.query
        response['message'] = ''
        # response['payload'] = [i.serialize for i in query.all()]
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
