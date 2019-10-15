'''
Transaction Endpoints
'''
import datetime
import json
import random
from flask import Blueprint, current_app, jsonify, request, abort
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.models import *
from src.util import validate_request_data

transactions = Blueprint('transactions', __name__)
#===============================================================================
# GET ALL TRANSACTION
@transactions.route('/', defaults={'id':None}, methods=['GET'])
@transactions.route('/<int:id>', methods=['GET'])
# @jwt_required
# @has_permission([])
def get_transactions(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        # TODO: make sure user has access to the project
        query = Transaction.query
        if id is None:
            if 'project_id' not in args.keys():
                raise ValueError('Please specify a Transaction ID in the URL or a Project ID as an argument for the transactions query.')
            query = query.filter_by(project_id=args['project_id']) if 'project_id' in args.keys() and args['project_id'].isdigit() else query
        else:
            # ID filter
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError('Transaction ID {} does not exist.'.format(id))

        # Set ORDER
        query = query.order_by('id')
        # Set LIMIT
        query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query
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
# Check if transaction locked
@transactions.route('/<int:id>/is_locked', methods=['GET'])
# @jwt_required
# @has_permission([])
def check_transaction_lock(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        # TODO: make sure user has access to the project
        if id is None:
            raise ValueError('Please specify a Transaction ID for the transactions query.')

        query = Transaction.find_by_id(id)
        if not query:
            raise ValueError('Transaction ID {} does not exist.'.format(id))

        response['payload'] = query.locked_transaction_user.username if query.locked_transaction_user else ''
    except ValueError as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200

#===============================================================================
# Lock Transaction
@transactions.route('/<int:id>/lock', methods=['PUT'])
@jwt_required
# @has_permission([])
def lock_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        # TODO: make sure user has access to the project
        query = Transaction.find_by_id(id)
        if not query:
            raise ValueError('Transaction ID {} does not exist.'.format(id))
        if query.locked_transaction_user and query.locked_user_id != current_user.id:
            raise ValueError('Transaction ID {} is already locked and not by you!'.format(id))

        if query.locked_user_id == current_user.id:
            response['message'] = 'You have already locked this transaction!'
        else:
            query.locked_user_id = current_user.id
            response['message'] = 'Transaction locked.'

        db.session.commit()
        response['payload'] = [Transaction.find_by_id(id).serialize]
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
# Unlock Transaction
@transactions.route('/<int:id>/unlock', methods=['PUT'])
@jwt_required
# @has_permission([])
def unlock_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        # TODO: make sure user has access to the project
        query = Transaction.find_by_id(id)
        if not query:
            raise ValueError('Transaction ID {} does not exist.'.format(id))
        if query.locked_transaction_user and query.locked_user_id != current_user.id:
            raise ValueError('Transaction ID {} is locked and not by you!'.format(id))

        if not query.locked_user_id:
            response['message'] = 'This transaction is already unlocked!'
        else:
            query.locked_user_id = None
            response['message'] = 'Transaction unlocked.'

        db.session.commit()
        response['payload'] = [Transaction.find_by_id(id).serialize]
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
# UPDATE A TRANSACTION information
@transactions.route('/<path:id>', methods=['PUT'])
@jwt_required
# @has_permission([])
def update_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # TODO: make sure user has access to the project
        # input validation
        request_types = {
            'codes': 'dict'
        }
        validate_request_data(data, request_types)

        # UPDATE user
        query = Transaction.find_by_id(id)
        if not query:
            raise ValueError('Transaction ID {} does not exist.'.format(id))

        if query.locked_transaction_user and query.locked_user_id != current_user.id:
            raise ValueError('Transaction ID {} is locked and not by you!'.format(id))
        if not query.locked_user_id:
            raise ValueError('Please lock transaction ID {} before updating!'.format(id))

        query.codes = data['codes']

        db.session.commit()
        response['payload'] = [Transaction.find_by_id(id).serialize]
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response), 200
