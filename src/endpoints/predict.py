'''
Predict Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from src.models import *

predict = Blueprint('predict', __name__)
#===============================================================================
# General
@predict.route('/', methods=['GET'])
def do_predict():
    response = { 'status': '', 'message': '', 'payload': [] }
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)
