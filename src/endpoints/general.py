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
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)
