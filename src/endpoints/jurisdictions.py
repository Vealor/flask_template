'''
Jurisdiction Endpoints
'''
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.models import Jurisdiction
from src.wrappers import has_permission, exception_wrapper

jurisdictions = Blueprint('jurisdictions', __name__)
#===============================================================================
# GET ALL JURISDICTIONS
@jurisdictions.route('/', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_jurisdictions():
    response = {'status': 'ok', 'message': '', 'payload': []}
    response['payload'] = Jurisdiction.list()
    return jsonify(response)
