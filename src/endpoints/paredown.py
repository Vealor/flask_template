'''
Paredown Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.util import validate_request_data

paredown = Blueprint('paredown', __name__)
#===============================================================================
# GET ALL Paredown rules
@paredown.route('/', methods=['GET'])
@paredown.route('/<int:id>', methods=['GET'])
# @jwt_required
def get_paredown_rules(id=None):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    try:

        if id:
            rule = ParedownRule.find_by_id(id)
            if rule:
                response['payload'] = rule.serialize
            else:
                raise ValueError("No paredown rule with ID {}".format(id))
        else:
            response['payload'] = [i.serialize for i in ParedownRule.query.all()]

    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200

#===============================================================================
# Create Paredown rules
@paredown.route('/', methods=['POST'])
# @jwt_required
def create_paredown_rule():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    try:
        # Validate the fields of the new paredown rule
        request_types = {
            'approver1' : 'int',
            'approver2' : 'int',
            'code': 'str',
            'comment': 'str',
            'is_core': 'bool',
            'is_active': 'bool'
        }
        validate_request_data(data, request_types)

        if data['code'] == '':
            raise ValueError("Cannot create paredown rule with no code.")

        # Validate each condition of the new paredown rule
        if len(data['conditions']) == 0:
            raise ValueError("Cannot create paredown rule with no conditions.")

        # Make sure valid user ids are used to approve paredown rules
        for approver_id in [data['approver1'], data['approver2']]:
            if approver_id == -1:   # '-1' indicates no approver specified.
                pass
            else:
                user = User.find_by_id(approver_id)
                if not user:
                    raise ValueError("User ID {} does not exist.".format(approver_id))
                else:
                    if not (user.role == Roles.tax_master or user.is_superuser):
                        raise ValueError("User ID {} is not a valid approver for Paredown rules.".format(user.id))

        request_types_conditions = {
            'field': 'str',
            'operator': 'str'
        }

        for cond in data['conditions']:
            validate_request_data(cond, request_types_conditions)

        # Create the new paredown rule
        new_paredown_rule = ParedownRule(
            approver1 = (None if data['approver1'] == -1 else data['approver1']),
            approver2 = (None if data['approver2'] == -1 else data['approver2']),
            code = data['code'],
            is_active = data['is_active'],
            is_core = data['is_core'],
            comment = data['comment']
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

        for lob_sec in data['lob_sectors']:
            new_paredown_lob = ParedownRuleLineOfBusinessSector(
                lob_sector = lob_sec,
                paredown_rule_id = new_paredown_rule.id
            )
            db.session.add(new_paredown_lob)
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
@paredown.route('/<int:id>', methods=['PUT'])
# @jwt_required
def update_paredown_rule(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    try:
        # Validate the fields of the updated paredown rule
        request_types = {
            'approver1' : 'int',
            'approver2' : 'int',
            'code': 'str',
            'comment': 'str',
            'is_core': 'bool',
            'is_active': 'bool'
        }
        validate_request_data(data, request_types)

        if data['code'] == '':
            raise ValueError("Cannot create paredown rule with no code.")

        # Validate each condition of the new paredown rule
        if len(data['conditions']) == 0:
            raise ValueError("Cannot create paredown rule with no conditions.")

        # Make sure valid user ids are used to approve paredown rules
        for approver_id in [data['approver1'], data['approver2']]:
            if approver_id == -1:   # '-1' indicates no approver specified.
                pass
            else:
                user = User.find_by_id(approver_id)
                if not user:
                    raise ValueError("User ID {} does not exist.".format(approver_id))
                else:
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
        query.is_core = data['is_core']
        query.approver1 = (None if data['approver1'] == -1 else data['approver1'])
        query.approver2 = (None if data['approver2'] == -1 else data['approver2'])


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

        lob_secs = ParedownRuleLineOfBusinessSector.query.filter_by(paredown_rule_id=id).all()
        for lob_sec in lob_secs:
            db.session.delete(lob_sec)
            db.session.flush()

        for lob_sec in data['lob_sectors']:
            new_paredown_lob = ParedownRuleLineOfBusinessSector(
                lob_sector = lob_sec,
                paredown_rule_id = query.id
            )
            db.session.add(new_paredown_lob)
            db.session.flush()

        db.session.commit()
        response['message'] = 'Successfully updated Paredown Rule ID {}.'.format(query.id)

    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200

#===============================================================================
# DELETE A PAREDOWN RULE
@paredown.route('/<int:id>', methods=['DELETE'])
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
