'''
Client Vendor Mater Endpoints
'''
from sqlalchemy import desc
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.models import *
from src.wrappers import has_permission, exception_wrapper

client_vendor_master = Blueprint('client_vendor_master', __name__)
#===============================================================================
# Get ClientVendorMaster information for project
@client_vendor_master.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_client_vendor_master(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    if 'project_id' not in args.keys():
        raise InputError('Please specify a Project ID as an argument for the query.')
    if not Project.find_by_id(args['project_id']):
        raise NotFoundError('Project does not exist.')

    query = CapsGen.query.order_by(desc(CapsGen.created))
    query = query.filter_by(project_id=args['project_id'])
    capsgen = query.first()
    if not capsgen:
        raise NotFoundError('There is no CapsGen for this project.')
    rows = SapLfa1.query.filter_by(capsgen_id=capsgen.id).all()
    response['payload'] = [row.data for row in rows]

    return jsonify(response), 200
