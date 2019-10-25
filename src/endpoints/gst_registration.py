'''
GST Registration Endpoints
'''
from flask import Blueprint, jsonify
from sqlalchemy import func
from src.models import *

gst_registration = Blueprint('gst_registration', __name__)
#===============================================================================
# Permission Check
@gst_registration.route('/', methods=['GET'])
def get_gst_registration():
    try:
        code = 500
        response = {'status': 'ok', 'message': '', 'payload': []}
        if SapLfa1.query.count() < 1:
            code = 404
            raise ValueError('No record found')
        # filter get the newset capgs for each project
        # TODO: dedup lib identify potencial similar project add another column duplicate flag (code)
        capsgens = db.session.query(func.max(CapsGen.id)).group_by(CapsGen.project_id)
        all_data = SapLfa1.query.filter(CapsGen.id.in_(capsgens)).all()
        response['payload']  = [row.data for row in all_data]
        code = 200
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'error'
        response['payload'] = []
    return jsonify(response), code
