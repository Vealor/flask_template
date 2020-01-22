'''
DataParam Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from src.core.models import db, DataParam
from src.errors import InputError, NotFoundError
from src.util import validate_request_data, create_log
from src.wrappers import has_permission, exception_wrapper

data_params = Blueprint('data_params', __name__)
#===============================================================================
# GET ALL DATA PARAMS
@data_params.route('/', defaults={'id': None}, methods=['GET'])
@data_params.route('/<int:id>', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_data_params(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    # TODO: make sure user has access to the project
    query = DataParam.query
    if id is None:
        if 'project_id' not in args.keys():
            raise InputError('Please specify a Project ID as an argument for the data_params query.')
        query = query.filter_by(project_id=args['project_id']) if 'project_id' in args.keys() and args['project_id'].isdigit() else query
    else:
        # ID filter
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('Data Parameter ID {} does not exist.'.format(id))

    # Set ORDER
    query = query.order_by('id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# UPDATE A Data Parameter information
@data_params.route('/<int:id>', methods=['PUT'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def update_data_params(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    # TODO: make sure user has access to the project
    # input validation
    request_types = {
        'value': ['list'],
        'is_many': ['bool']
    }
    validate_request_data(data, request_types)
    if [x for x in data['value'] if not isinstance(x, str)]:
        raise InputError("Value data must be a list of strings.")

    # UPDATE user
    query = DataParam.find_by_id(id)
    if not query:
        raise NotFoundError('Data Parameter ID {} does not exist.'.format(id))

    query.value = data['value']
    query.is_many = data['is_many']

    db.session.commit()
    response['payload'] = [DataParam.find_by_id(id).serialize]
    create_log(current_user, 'modify', 'User updated Data Parameeter', 'ID: ' + str(id))

    return jsonify(response), 200
