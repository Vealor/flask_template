'''
Log Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from src.models import Log
from src.wrappers import has_permission, exception_wrapper

logs = Blueprint('logs', __name__)
#===============================================================================
# GET ALL LOGS
@logs.route('/', methods=['GET'])
@jwt_required
# PERMISSION IT ADMIN
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_logs():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = Log.query
    # Set ORDER
    query = query.order_by(desc('timestamp'))
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)
