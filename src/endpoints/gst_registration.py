'''
GST Registration Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from sqlalchemy import func
from src.models import *
from src.wrappers import has_permission, exception_wrapper

gst_registration = Blueprint('gst_registration', __name__)
#===============================================================================
# Permission Check
@gst_registration.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_gst_registration():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    # filter get the newset capgs for each project
    # TODO: dedup lib identify potencial similar project add another column duplicate flag (code)
    capsgens = db.session.query(func.max(CapsGen.id)).group_by(CapsGen.project_id)
    all_data = GstRegistration.query.filter(CapsGen.id.in_(capsgens)).all()
    response['payload']  = [row.data for row in all_data]

    return jsonify(response), 200
