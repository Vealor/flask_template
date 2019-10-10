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
def get_lob_sectors():
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        response['payload'] = LineOfBusinessSectors.list()
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response)
