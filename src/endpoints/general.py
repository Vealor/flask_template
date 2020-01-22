'''
General Endpoints
'''
from flask import Blueprint, current_app, jsonify
from src.wrappers import exception_wrapper

general = Blueprint('general', __name__)
#===============================================================================
# General
@general.route('/', methods=['GET'])
@exception_wrapper
def default():
    response = {'status': 'ok', 'message': '', 'payload': []}

    response['VERSION'] = current_app.config['VERSION']
    response['payload'] = []
    return jsonify(response)
