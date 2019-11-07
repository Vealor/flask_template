'''
Tax Rate Endpoints
'''
from sqlalchemy import desc
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.models import *
from src.wrappers import has_permission, exception_wrapper

tax_rates = Blueprint('tax_rates', __name__)
#===============================================================================
# Get Tax Rates
@tax_rates.route('/', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_tax_rates():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    if 'project_id' not in args.keys():
        raise InputError('Please specify a Project ID as an argument for the query.')
    if not Project.find_by_id(args['project_id']):
        raise NotFoundError('Project does not exist.')

    # check if caps_gen exist, if exist proceed, if not send back error message
    capsgen = CapsGen.query.filter_by(project_id=args['project_id']).order_by(desc(CapsGen.id)).first()
    if not capsgen:
        raise InputError("Caps has not been generated, Please generate caps first.")
    rows = SapT007s.query.filter_by(capsgen_id=capsgen.id).all()
    response['payload'] = [row.data for row in rows]

    return jsonify(response), 200
