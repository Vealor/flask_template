'''
DataMapping Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.errors import InputError, NotFoundError
from src.models import db, DataMapping
from src.util import validate_request_data
from src.wrappers import has_permission, exception_wrapper

data_mappings = Blueprint('data_mappings', __name__)
#===============================================================================
# GET ALL DATA MAPPINGS
@data_mappings.route('/', defaults={'id': None}, methods=['GET'])
@data_mappings.route('/<int:id>', methods=['GET'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_data_mappings(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = DataMapping.query
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('ID {} does not exist.'.format(id))
    else:
        if 'caps_gen_id' not in args.keys():
            raise InputError('Please specify a caps_gen_id ID as an argument for the data_mappings query.')
        query = query.filter_by(caps_gen_id=args['caps_gen_id'])

    # Set ORDER
    query = query.order_by('caps_gen_id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)

#===============================================================================
# CREATE NEW DATA MAPPING
# not done as new mappings can't be created
# they are made during the CAPSGen process in /caps_gen/init

#===============================================================================
# UPDATE DATA MAPPING
@data_mappings.route('/<int:id>', methods=['PUT'])
@jwt_required
@exception_wrapper()
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def update_data_mapping(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    request_types = {
        'table_name': ['str', ''],
        'column_name': ['str', '']
    }
    validate_request_data(data, request_types)

    # UPDATE data mapping
    query = DataMapping.find_by_id(id)
    if not query:
        raise NotFoundError('Data Mapping ID {} does not exist.'.format(id))

    query.table_name = data['table_name']
    query.column_name = data['column_name']

    db.session.commit()
    response['message'] = 'Updated data_mapping with id {}'.format(id)
    response['payload'] = [DataMapping.find_by_id(id).serialize]
    # no logging required

    return jsonify(response)

#===============================================================================
# DELETE DATA MAPPING
# not done as mappings are only deleted through project deletion
