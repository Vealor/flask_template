'''
Jurisdiction Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.errors import *
from src.models import *
from src.wrappers import has_permission, exception_wrapper

lob_sectors = Blueprint('lob_sectors', __name__)
#===============================================================================
# GET ALL LineOfBusinessSectors
@lob_sectors.route('/', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_lob_sectors():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['payload'] = LineOfBusinessSectors.list()
    return jsonify(response)
