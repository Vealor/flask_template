'''
Paredown Endpoints
'''
import json
import random
import sqlalchemy
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from sqlalchemy.dialects import postgresql
from src.errors import *
from src.models import *
from src.util import validate_request_data
from src.wrappers import has_permission, exception_wrapper

paredown_rules = Blueprint('paredown_rules', __name__)
#===============================================================================
# GET ALL Paredown rules
@paredown_rules.route('/', defaults={'id':None}, methods=['GET'])
@paredown_rules.route('/<int:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_paredown_rules(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = ParedownRule.query
    if id:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError("Paredown rule ID {} does not exist.".format(id))
    # Set ORDER
    query = query.order_by('id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# Create Paredown rules
@paredown_rules.route('/', methods=['POST'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def create_paredown_rule():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    request_types = {
        'approver1_id' : ['int','NoneType'],
        'approver2_id' : ['int','NoneType'],
        'code_id': ['int'],
        'is_active': ['bool']
    }
    validate_request_data(data, request_types)

    if len(data['conditions']) == 0:
        raise InputError("Cannot create paredown rule with no conditions.")
    request_types_conditions = {
        'field': ['str'],
        'operator': ['str']
    }
    for cond in data['conditions']:
        validate_request_data(cond, request_types_conditions)

    # Make sure valid user ids are used to approve paredown rules
    for approver_id in filter(None, [data['approver1_id'], data['approver2_id']]):
        user = User.find_by_id(approver_id)
        if not user:
            raise InputError("User ID {} does not exist.".format(approver_id))
        if not (user.role == Roles.tax_master or user.is_superuser):
            raise InputError("User ID {} is not a valid approver for Paredown rules.".format(user.id))

    codecheck = Code.find_by_id(data['code_id'])
    if not codecheck:
        raise InputError("Code ID {} does not exist.".format(data['code_id']))

    lob_sectors = []
    # Create the new paredown rule
    for lob_sec in data['lob_sectors']:
        if lob_sec not in LineOfBusinessSectors.__members__:
            raise InputError('Specified lob_sec does not exist.')
        if LineOfBusinessSectors[lob_sec] not in lob_sectors:
            lob_sectors.append(LineOfBusinessSectors[lob_sec])

    new_paredown_rule = ParedownRule(
        paredown_rule_approver1_id = data['approver1_id'],
        paredown_rule_approver2_id = data['approver2_id'],
        code_id = data['code_id'],
        is_core = data['is_core'],
        is_active = data['is_active'],
        comment = data['comment'],
        lob_sectors = sqlalchemy.cast(lob_sectors, postgresql.ARRAY(postgresql.ENUM(LineOfBusinessSectors)))
    )
    db.session.add(new_paredown_rule)
    db.session.flush()

    # Create the conditions for the paredown rule
    for cond in data['conditions']:
        new_paredown_condition = ParedownRuleCondition(
            field = cond['field'],
            operator = cond['operator'],
            value = cond['value'],
            paredown_rule_id = new_paredown_rule.id
        )
        db.session.add(new_paredown_condition)
        db.session.flush()

    db.session.commit()
    response['message'] = 'Created Paredown Rule ID with {}.'.format(new_paredown_rule.id)
    response['payload'] = [ParedownRule.find_by_id(new_paredown_rule.id).serialize]

    return jsonify(response), 201

#===============================================================================
# Update a Paredown rule
@paredown_rules.route('/<int:id>', methods=['PUT'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def update_paredown_rule(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # Validate each condition of the new paredown rule
    if len(data['conditions']) == 0:
        raise InputError("Cannot update paredown rule with no conditions.")
    request_types = {
        'approver1_id' : ['int','NoneType'],
        'approver2_id' : ['int','NoneType'],
        'code_id': ['int'],
        'is_active': ['bool']
    }
    validate_request_data(data, request_types)
    request_types_conditions = {
        'field': ['str'],
        'operator': ['str'],
        'value': ['str']
    }
    for cond in data['conditions']:
        validate_request_data(cond, request_types_conditions)

    # Make sure valid user ids are used to approve paredown rules
    for approver_id in filter(None, [data['approver1_id'], data['approver2_id']]):
        user = User.find_by_id(approver_id)
        if not user:
            raise InputError("User ID {} does not exist.".format(approver_id))
        if not (user.role == Roles.tax_master or user.is_superuser):
            raise InputError("User ID {} is not a valid approver for Paredown rules.".format(user.id))

    query = ParedownRule.find_by_id(id)
    if not query:
        raise InputError("Paredown Rule ID {} does not exist.".format(id))

    codecheck = Code.find_by_id(data['code_id'])
    if not codecheck:
        raise InputError("Code ID {} does not exist.".format(data['code_id']))

    query.code_id = data['code_id']
    query.comment = data['comment']
    query.is_core = data['is_core']
    query.is_active = data['is_active']
    query.paredown_rule_approver1_id = data['approver1_id']
    query.paredown_rule_approver2_id = data['approver2_id']

    lob_sectors = []
    # Create the new paredown rule
    for lob_sec in data['lob_sectors']:
        if lob_sec not in LineOfBusinessSectors.__members__:
            raise InputError('Specified lob_sec does not exist.')
        if LineOfBusinessSectors[lob_sec] not in lob_sectors:
            lob_sectors.append(LineOfBusinessSectors[lob_sec])
    query.lob_sectors = sqlalchemy.cast(lob_sectors, postgresql.ARRAY(postgresql.ENUM(LineOfBusinessSectors)))

    # Delete and recreate the paredown conditions
    conditions = ParedownRuleCondition.query.filter_by(paredown_rule_id=id).all()
    for cond in conditions:
        db.session.delete(cond)
        db.session.flush()

    for cond in data['conditions']:
        new_paredown_condition = ParedownRuleCondition(
            field = cond['field'],
            operator = cond['operator'],
            value = cond['value'],
            paredown_rule_id = query.id
        )
        db.session.add(new_paredown_condition)
        db.session.flush()

    db.session.commit()
    response['message'] = 'Updated Paredown Rule ID with {}.'.format(query.id)
    response['payload'] = [ParedownRule.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# DELETE A PAREDOWN RULE
@paredown_rules.route('/<int:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def delete_paredown_rule(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = ParedownRule.find_by_id(id)
    if not query:
        raise NotFoundError("Paredown Rule ID {} does not exist.".format(id))

    pd_rule = query.serialize
    db.session.delete(query)
    db.session.commit()

    response['message'] = 'Deleted Paredown rule ID {}'.format(pd_rule['id'])
    response['payload'] = [pd_rule]

    return jsonify(response), 200
