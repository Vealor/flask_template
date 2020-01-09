'''
Jurisdiction Endpoints
'''
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.models import LineOfBusinessSectors
from src.wrappers import has_permission, exception_wrapper

lob_sectors = Blueprint('lob_sectors', __name__)
#===============================================================================
# GET ALL LineOfBusinessSectors
@lob_sectors.route('/', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_lob_sectors():
    response = {'status': 'ok', 'message': '', 'payload': []}
    response['payload'] = LineOfBusinessSectors.list()
    return jsonify(response)
