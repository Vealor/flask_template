'''
Jurisdiction Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *

lob_sectors = Blueprint('lob_sectors', __name__)
#===============================================================================
# GET ALL LineOfBusinessSectors
@lob_sectors.route('/', methods=['GET'])
# @jwt_required
def default():
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        response['message'] = ''
        response['payload'] = LineOfBusinessSectors.list()
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
