import json
import random
from flask import Blueprint, current_app, jsonify, request
from src.models import *
from src.wrappers import has_permission, exception_wrapper

data_params = Blueprint('data_params', __name__)

@data_params.route('/data_params/<path:project_id>', methods=['GET'])
@exception_wrapper()
def view_tables(project_id):
    response = {'status': 'ok', 'message': {}, 'payload': []}

    query = data_params.query

    # project_id filter
    if project_id is not None and isinstance(project_id, int):
        project = Project.find_by_id(project_id)
    else:
        raise ValueError('Project ID {} does not exist.'.format(project_id))

    capsgen_id = CapsGen.query.filter(CapsGen.project_id == project_id).order_by(desc(CapsGen.id)).first().id
    if not capsgen_id:
        raise ValueError('CAPS Generation has not been run on this project yet. Please run CAPS Generation from source data upload.')

    #table filter
    if table is not None:
        tableclass = eval('Sap' + str(table.lower().capitalize()))
        columndata = tableclass.query.with_entities(getattr(tableclass, 'data')).filter(tableclass.capsgen_id == capsgen_id).all()
        response['payload'] = columndata
        response['message'] = str(table) + ' has been accessed.'

    return jsonify(response), 200


@projects.route('/<path:id>', methods=['PUT'])
# @jwt_required
@exception_wrapper()
def update_project(id):
    data = request.get_json()

    # input validation
    request_types = {
        'name': 'str',
        'is_paredown_locked': 'bool',
        'is_completed': 'bool',
        'client_id': 'int',
        'project_users': 'list',
        'engagement_partner_id': 'int',
        'engagement_manager_id': 'int',
        'tax_scope': 'dict',
        'engagement_scope': 'dict'
    }
    validate_request_data(data, request_types)
