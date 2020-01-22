'''
Role Endpoints
'''
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.models import Roles
from src.wrappers import has_permission, exception_wrapper

roles = Blueprint('roles', __name__)
#===============================================================================
# GET ALL Roles
@roles.route('/', methods=['GET'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_roles():
    response = {'status': 'ok', 'message': '', 'payload': []}
    response['payload'] = Roles.list()
    return jsonify(response)
