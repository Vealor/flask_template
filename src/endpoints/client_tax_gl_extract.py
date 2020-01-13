'''
Client Tax GL Extract Endpoints
'''
from sqlalchemy import desc
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.errors import *
from src.models import *
from src.wrappers import has_permission, exception_wrapper

client_tax_gl_extract = Blueprint('client_tax_gl_extract', __name__)
#===============================================================================
# Get Client_tax_gl_extract information for project
@client_tax_gl_extract.route('/', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_client_vendor_master():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    if 'project_id' not in args.keys():
        raise InputError('Please specify a Project ID as an argument for the query.')
    if not Project.find_by_id(args['project_id']):
        raise NotFoundError('Project does not exist.')

    query = CapsGen.query.order_by(desc(CapsGen.created))
    query = query.filter_by(project_id=args['project_id'], is_completed=True)

    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)
    caps_gen = query.first()
    if not caps_gen:
        raise NotFoundError('There is no CapsGen for this project.')
    rows = SapTaxGLExtract.query.filter_by(caps_gen_id=caps_gen.id).all()
    response['payload'] = [row.serialize for row in rows]

    return jsonify(response), 200
