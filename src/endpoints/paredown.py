'''
Paredown Endpoints
'''
import json
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from src.paredown.paredown_rule import ParedownRuleObject
from src.paredown.paredown_condition import ParedownConditionObject
from src.util import validate_request_data

paredown = Blueprint('paredown', __name__)
#===============================================================================
# GET ALL Paredown rules
@paredown.route('/', methods=['GET'])
# @jwt_required
def get_paredown_rules():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    try:
        query = ParedownRule.query
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
@paredown.route('/', methods=['POST'])
# @jwt_required
def create_paredown_rule():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    try:
        # Validate the fields of the new paredown rule
        request_types = {
            'code': 'str',
            'comment': 'str',
            'is_core': 'bool'
        }
        validate_request_data(data, request_types)

        if data['code'] == '':
            raise ValueError("Cannot create paredown rule with no code.")

        # Validate each condition of the new paredown rule
        if len(data['conditions']) == 0:
            raise ValueError("Cannot create paredown rule with no conditions.")

        request_types_conditions = {
            'field': 'str',
            'operator': 'str'
        }

        for cond in data['conditions']:
            validate_request_data(cond, request_types_conditions)

        # Create the new paredown rule
        new_paredown_rule = ParedownRule(
            code = data['code'],
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
# Apply Paredown rules
@paredown.route('/apply/', methods=['POST'])
# @jwt_required
def apply_paredown_rules(df=None):
    response = { 'status': 'ok', 'message': '', 'payload': [] }


    try:
        # Retrieve and create the rule objects
        paredown_rule_entries = ParedownRule.query
        rules = []
        for pr in paredown_rule_entries:
            i = pr.id
            conds = ParedownRuleCondition.query.filter_by(paredown_rule_id=i).all()
            pcs = [ParedownConditionObject(*(p.field,p.operator,p.value)) for p in conds]
            rules.append(ParedownRuleObject(pcs, pr.code, pr.comment))

        # Now apply the rules to the data and append the codes as appropriate
        paredown_codes = {i: set('') for i in range(len(df))}
        paredown_comments = {i: set('') for i in range(len(df))}
        for r in rules:
            inds = list(df.loc[r.apply_to_data(df)].index)
            for i in inds:
                paredown_codes[i] |= set([str(r.code)])
                paredown_comments[i] |= set([str(r.comment) if r.comment else ''])

        paredown_codes = [','.join(x) for x in paredown_codes.values()]
        paredown_comments = [','.join(x) for x in paredown_comments.values()]
        response['payload'] = {'codes': paredown_codes, 'comments': paredown_comments}
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200

#===============================================================================
# Update a Paredown rule
@paredown.route('/<path:id>', methods=['PUT'])
# @jwt_required
def update_paredown_rule(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    try:
        # Validate the fields of the updated paredown rule
        request_types = {
            'code': 'str',
            'comment': 'str',
            'is_core': 'bool'
        }
        validate_request_data(data, request_types)

        if data['code'] == '':
            raise ValueError("Cannot create paredown rule with no code.")

        # Validate each condition of the new paredown rule
        if len(data['conditions']) == 0:
            raise ValueError("Cannot create paredown rule with no conditions.")

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
        query.is_core = data['is_core']

        # Delete and recreate the paredown conditions
        conditions = ParedownRuleCondition.query.filter_by(paredown_rule_id=id).all()
        for cond in conditions:
            db.session.delete(cond)

        new_conditions = data['conditions']
        for cond in new_conditions:
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
