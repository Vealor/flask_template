'''
General Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from src.models import *

general = Blueprint('general', __name__)
#===============================================================================
# General
@general.route('/', methods=['GET'])
def default():
    response = { 'status': '', 'message': '', 'payload': [] }
    try:
        response['VERSION'] = current_app.config['VERSION']

        response['status'] = 'ok'
        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response)
