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
        response = {'status': 'ok', 'message': '', 'payload': []}
        if SapLfa1.query.count() < 1:
            raise ValueError('No record found')
        # filter get the newset capgs for each project
        # TODO: dedup lib identify potencial similar project add another column duplicate flag (code)
        capsgens = db.session.query(func.max(CapsGen.id)).group_by(CapsGen.project_id)
        all_data = SapLfa1.query.filter(CapsGen.id.in_(capsgens)).all()
        response['payload']  = [row.data for row in all_data]
    except ValueError as e:
        response = {'status': 'error', 'message': str(e), 'payload': []}
        return jsonify(response), 404
    except Exception as e:
        response = {'status': 'error', 'message': str(e), 'payload': []}
        return jsonify(response), 500
    return jsonify(response), 200
