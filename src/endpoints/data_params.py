import json
import random
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.wrappers import has_permission, exception_wrapper

data_params = Blueprint('data_params', __name__)
#===============================================================================
# GET ALL DATA PARAMS
@data_params.route('/', defaults={'id':None}, methods=['GET'])
@data_params.route('/<int:id>', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_transactions(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    # TODO: make sure user has access to the project
    query = DataParam.query
    if id is None:
        if 'project_id' not in args.keys():
            raise ValueError('Please specify a Project ID as an argument for the data_params query.')
        query = query.filter_by(project_id=args['project_id']) if 'project_id' in args.keys() and args['project_id'].isdigit() else query
    else:
        # ID filter
        query = query.filter_by(id=id)
        if not query.first():
            raise ValueError('Data Parameter ID {} does not exist.'.format(id))

    # Set ORDER
    query = query.order_by('id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200





# only need get and update
# need to add base creation of params for a project on post project
# update does only value and is_many:
#   value = db.Column(postgresql.ARRAY(db.String), nullable=True)
#   is_many = db.Column(db.Boolean, nullable=False)






# @data_params.route('/<path:id>', methods=['PUT'])
# # @jwt_required
# @exception_wrapper()
# def update_params(id):
#     data = request.get_json()
#
#     # input validation
#     request_types = {
#         'name': ['str'],
#         'is_paredown_locked': ['bool'],
#         'is_completed': ['bool'],
#         'client_id': ['int'],
#         'project_users': ['list'],
#         'engagement_partner_id': ['int'],
#         'engagement_manager_id': ['int'],
#         'tax_scope': ['dict'],
#         'engagement_scope': ['dict']
#     }
#     validate_request_data(data, request_types)
#
#     return jsonify(response), 200
