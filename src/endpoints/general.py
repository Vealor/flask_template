'''
General Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.wrappers import has_permission, exception_wrapper

general = Blueprint('general', __name__)
#===============================================================================
# General
@general.route('/', methods=['GET'])
@exception_wrapper()
def default():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    response['VERSION'] = current_app.config['VERSION']
    return jsonify(response)
