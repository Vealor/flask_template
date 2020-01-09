'''
CDMLabel Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import CDMLabel
from src.wrappers import has_permission, exception_wrapper

cdm_labels = Blueprint('cdm_labels', __name__)
#===============================================================================
# GET ALL DATA MAPPINGS
@cdm_labels.route('/', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_cdm_labels():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = CDMLabel.query
    # Set ORDER
    query = query.order_by('script_label')

    if 'caps_table' in args.keys():
        output = {}
        for i in query.all():
            output[i.script_label] = {'display_name': i.display_name, 'caps_interface': i.caps_interface.value if i.caps_interface else None}
        response['payload'] = output
    else:
        response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)
