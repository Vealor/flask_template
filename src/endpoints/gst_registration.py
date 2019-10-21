'''
General Endpoints
'''
from flask import Blueprint, jsonify
from src.models import SapLfa1

gst_registration = Blueprint('gst_registration', __name__)
#===============================================================================
# General
@gst_registration.route('/', methods=['GET'])
def get_gst_registration():
    try:
        code = 500
        response = {'status': 'ok', 'message': '', 'payload': []}
        all_data_count = SapLfa1.query.count()
        if all_data_count < 1:
            code = 404
            raise ValueError('Non record found')
        all_data = SapLfa1.query.all()
        gst_registration_data = [row.data for row in all_data]
        response['payload'] = gst_registration_data
        code = 200
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'error'
        response['payload'] = []
    return jsonify(response), code
