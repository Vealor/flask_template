'''
GST Registration Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from src.core.models import db
from src.ind_tax.models import CapsGen, GstRegistration
from src.wrappers import has_permission, exception_wrapper

gst_registration = Blueprint('gst_registration', __name__)
#===============================================================================
# Permission Check
@gst_registration.route('/', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_gst_registration():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    # filter get the newset capgs for each project
    # TODO: dedup lib identify potencial similar project add another column duplicate flag (code)
    caps_gens = db.session.query(func.max(CapsGen.id)).group_by(CapsGen.project_id)

    query = GstRegistration.query.filter(CapsGen.id.in_(caps_gens))

    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200
