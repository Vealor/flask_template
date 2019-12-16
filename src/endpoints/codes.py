'''
Code Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.errors import *
from src.models import *
from src.wrappers import has_permission, exception_wrapper

codes = Blueprint('codes', __name__)
#===============================================================================
# GET ALL CODES
@codes.route('/', methods=['GET'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_codes():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = Code.query
    # Set ORDER
    query = query.order_by('code_number')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]
    return jsonify(response)
