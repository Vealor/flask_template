'''
Paredown Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

paredown_rules = Blueprint('paredown_rules', __name__)
#===============================================================================
# GET ALL Paredown rules
@paredown_rules.route('/', defaults={'id':None}, methods=['GET'])
@paredown_rules.route('/<int:id>', methods=['GET'])
# @jwt_required
def get_paredown_rules(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = ParedownRule.query
        if id:
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError("Paredown rule ID {} does not exist.".format(id))
        # Set ORDER
        query = query.order_by('id')
        # Set LIMIT
        query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
        # Set OFFSET
        query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

        response['payload'] = [i.serialize for i in query.all()]
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200

#===============================================================================
# Create Paredown rules
@paredown_rules.route('/', methods=['POST'])
# @jwt_required
def create_paredown_rule():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    try:
        # Validate the fields of the new paredown rule
        request_types = {
            #'approver1_id' : 'int',
            #'approver2_id' : 'int',
            'code': 'int',
            'is_active': 'bool'
        }
        validate_request_data(data, request_types)

        # Validate each condition of the new paredown rule
        if len(data['conditions']) == 0:
            raise ValueError("Cannot create paredown rule with no conditions.")

        # Make sure valid user ids are used to approve paredown rules
        for approver_id in filter(None, [data['approver1_id'], data['approver2_id']]):
            user = User.find_by_id(approver_id)
            if not user:
                raise ValueError("User ID {} does not exist.".format(approver_id))
            if not (user.role == Roles.tax_master or user.is_superuser):
                raise ValueError("User ID {} is not a valid approver for Paredown rules.".format(user.id))

        request_types_conditions = {
            'field': 'str',
            'operator': 'str'
        }

        for cond in data['conditions']:
            validate_request_data(cond, request_types_conditions)

        # Create the new paredown rule
        for lob_sec in data['lob_sectors']:
            if lob_sec not in LineOfBusinessSectors.__members__:
                raise ValueError('Specified lob_sec does not exist.')
        new_paredown_rule = ParedownRule(
            paredown_rule_approver1_id = data['approver1_id'],
            paredown_rule_approver2_id = data['approver2_id'],
            code = data['code'],
            is_active = data['is_active'],
            comment = data['comment'],
            lob_sectors = data['lob_sectors']
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

        response['message'] = 'New paredown rule ID {} added.'.format(new_paredown_rule.id)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 201

#===============================================================================
# Update a Paredown rule
@paredown_rules.route('/<int:id>', methods=['PUT'])
# @jwt_required
def update_paredown_rule(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    try:
        # Validate the fields of the updated paredown rule
        request_types = {
            #'approver1_id' : 'int',
            #'approver2_id' : 'int',
            'code': 'int',
            'is_active': 'bool'
        }
        validate_request_data(data, request_types)

        # Validate each condition of the new paredown rule
        if len(data['conditions']) == 0:
            raise ValueError("Cannot create paredown rule with no conditions.")

        # Make sure valid user ids are used to approve paredown rules
        for approver_id in filter(None, [data['approver1_id'], data['approver2_id']]):
            user = User.find_by_id(approver_id)
            if not user:
                raise ValueError("User ID {} does not exist.".format(approver_id))
            if not (user.role == Roles.tax_master or user.is_superuser):
                raise ValueError("User ID {} is not a valid approver for Paredown rules.".format(user.id))

        request_types_conditions = {
            'field': 'str',
            'operator': 'str'
        }

        for cond in data['conditions']:
            validate_request_data(cond, request_types_conditions)


        query = ParedownRule.find_by_id(id)
        if not query:
            raise ValueError("Pareddown Rule ID {} does not exist.".format(id))
        query.code = data['code']
        query.comment = data['comment']
        query.is_active = data['is_active']
        query.paredown_rule_approver1_id = data['approver1_id']
        query.paredown_rule_approver2_id = data['approver2_id']
        for lob_sec in data['lob_sectors']:
            if lob_sec not in LineOfBusinessSectors.__members__:
                raise ValueError('Specified lob_sec does not exist.')
        query.lob_sectors = data['lob_sectors']

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
        response['message'] = 'Successfully updated Paredown Rule ID {}.'.format(query.id)

    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200

#===============================================================================
# DELETE A PAREDOWN RULE
@paredown_rules.route('/<int:id>', methods=['DELETE'])
# @jwt_required
def delete_paredown_rule(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:

        query = ParedownRule.find_by_id(id)
        if not query:
            raise ValueError("Paredown Rule ID {} does not exist.".format(id))

        pd_rule = query.serialize
        db.session.delete(query)
        db.session.commit()

        response['message'] = 'Deleted Paredown rule ID {}'.format(pd_rule['id'])
        response['payload'] = [pd_rule]
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200
