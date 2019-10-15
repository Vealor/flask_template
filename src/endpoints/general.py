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
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    try:
        response['VERSION'] = current_app.config['VERSION']
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response)
