'''
Error Categories Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from src.models import ErrorCategory
from src.wrappers import has_permission, exception_wrapper

error_categories = Blueprint('error_categories', __name__)
#===============================================================================
# GET ALL Error Categories
@error_categories.route('/', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_error_categories():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = ErrorCategory.query
    # Set ORDER
    query = query.order_by(desc('id'))
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)
