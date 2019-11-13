'''
CDMLabel Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.errors import *
from src.models import *
from src.wrappers import has_permission, exception_wrapper

cdm_labels = Blueprint('cdm_labels', __name__)
#===============================================================================
# GET ALL DATA MAPPINGS
@cdm_labels.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_cdm_labels():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CDMLabel.query
    # Set ORDER
    query = query.order_by('script_label')

    # Set LIMIT
    if 'caps_table' in args.keys():
        output = {}
        for i in query.all():
            output[i.script_label]={'display_name':i.display_name,'caps_interface':i.caps_interface.value if i.caps_interface else None}
        response['payload'] = output
    else:
        response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)
