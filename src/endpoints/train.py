'''
Train Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import *

train = Blueprint('train', __name__)
#===============================================================================
# General
@train.route('/', methods=['POST'])
@jwt_required
def do_train():
    response = { 'status': '', 'message': '', 'payload': []}
    data = request.get_json()
    if request.method == 'POST':
        print(data)
        response['data'] = data
    return jsonify(response), 202
