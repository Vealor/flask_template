'''
Transaction Endpoints
'''
import datetime
import json
import random
from flask import Blueprint, current_app, jsonify, request, abort
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from src.errors import *
from src.models import *
from src.util import validate_request_data
from src.wrappers import has_permission, exception_wrapper

transactions = Blueprint('transactions', __name__)
#===============================================================================
# GET ALL TRANSACTION
@transactions.route('/', defaults={'id':None}, methods=['GET'])
@transactions.route('/<int:id>', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_transactions(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    # TODO: make sure user has access to the project
    query = Transaction.query
    if id is None:
        if 'project_id' not in args.keys():
            raise InputError('Please specify a Transaction ID in the URL or a Project ID as an argument for the transactions query.')
        query = query.filter_by(project_id=args['project_id']) if 'project_id' in args.keys() and args['project_id'].isdigit() else query
    else:
        # ID filter
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('Transaction ID {} does not exist.'.format(id))

    # Set ORDER
    query = query.order_by('id')
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# Check if transaction locked
@transactions.route('/<int:id>/is_locked', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def check_transaction_lock(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    # TODO: make sure user has access to the project
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))

    response['payload'] = query.locked_transaction_user.username if query.locked_transaction_user else ''

    return jsonify(response), 200

#===============================================================================
# Lock Transaction
@transactions.route('/<int:id>/lock', methods=['PUT'])
@jwt_required
# @has_permission([])
@exception_wrapper()
def lock_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    # TODO: make sure user has access to the project
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))
    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is already locked and not by you!'.format(id))
    if query.approved_transaction_user:
        raise InputError('Transaction ID {} is already approved! Unapprove to lock and make changes.'.format(id))

    if query.locked_user_id == current_user.id:
        response['message'] = 'You have already locked this transaction!'
    else:
        query.locked_user_id = current_user.id
        response['message'] = 'Transaction locked.'

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# Unlock Transaction
@transactions.route('/<int:id>/unlock', methods=['PUT'])
@jwt_required
# @has_permission([])
@exception_wrapper()
def unlock_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    # TODO: make sure user has access to the project
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))
    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is locked and not by you!'.format(id))

    if not query.locked_user_id:
        response['message'] = 'This transaction is already unlocked!'
    else:
        query.locked_user_id = None
        response['message'] = 'Transaction unlocked.'

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200


#===============================================================================
# Approve Transaction
@transactions.route('/<int:id>/approve', methods=['PUT'])
@jwt_required
# @has_permission([])
@exception_wrapper()
def approve_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    # TODO: make sure user has access to the project
    #       make sure user has permission to approve
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))
    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is currently locked and not by you!'.format(id))
    if query.locked_user_id == current_user.id:
        raise InputError('Transaction ID {} is currently locked by you! Please unlock before approval.'.format(id))

    if query.approved_user_id == current_user.id:
        response['message'] = 'You have already approved this transaction!'
    else:
        query.approved_user_id = current_user.id
        response['message'] = 'Transaction approved.'

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# UnApprove Transaction
@transactions.route('/<int:id>/unapprove', methods=['PUT'])
@jwt_required
# @has_permission([])
@exception_wrapper()
def unapprove_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    # TODO: make sure user has access to the project
    #       make sure user has permission to unapprove
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))
    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is currently locked and not by you!'.format(id))

    # TODO: check if use can even unapprove the given transaction

    if not query.approved_user_id:
        response['message'] = 'This transaction is already unapproved!'
    else:
        query.approved_user_id = None
        response['message'] = 'Transaction unapproved.'

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# UPDATE A TRANSACTION information
@transactions.route('/<int:id>', methods=['PUT'])
@jwt_required
# @has_permission([])
@exception_wrapper()
def update_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # TODO: make sure user has access to the project
    # input validation
    request_types = {
        'gst_hst_code_id': ['int'],
        'gst_hst_notes': ['str'],
        'gst_hst_recoveries': ['float'],
        'gst_hst_error_type': ['str'],
        'gst_hst_coded_by_id': ['int'],
        'gst_hst_signed_off_by_id': ['int'],

        'qst_code_id': ['int'],
        'qst_notes': ['str'],
        'qst_recoveries': ['float'],
        'qst_error_type': ['str'],
        'qst_coded_by_id': ['int'],
        'qst_signed_off_by_id': ['int'],

        'pst_code_id': ['int'],
        'pst_notes': ['str'],
        'pst_recoveries': ['float'],
        'pst_error_type': ['str'],
        'pst_coded_by_id': ['int'],
        'pst_signed_off_by_id': ['int'],

        'apo_code_id': ['int'],
        'apo_notes': ['str'],
        'apo_recoveries': ['float'],
        'apo_error_type': ['str'],
        'apo_coded_by_id': ['int'],
        'apo_signed_off_by_id': ['int']
    }
    validate_request_data(data, request_types)

    # UPDATE user
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))

    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is locked and not by you!'.format(id))
    if not query.locked_user_id:
        raise InputError('Please lock transaction ID {} before updating!'.format(id))

    query.gst_hst_code_id = data['gst_hst_code_id']
    query.gst_hst_notes = data['gst_hst_notes']
    query.gst_hst_recoveries = data['gst_hst_recoveries']
    query.gst_hst_error_type = data['gst_hst_error_type']
    query.gst_hst_coded_by_id = data['gst_hst_coded_by_id']
    query.gst_hst_signed_off_by_id = data['gst_hst_signed_off_by_id']
    query.qst_code_id = data['qst_code_id']
    query.qst_notes = data['qst_notes']
    query.qst_recoveries = data['qst_recoveries']
    query.qst_error_type = data['qst_error_type']
    query.qst_coded_by_id = data['qst_coded_by_id']
    query.qst_signed_off_by_id = data['qst_signed_off_by_id']
    query.pst_code_id = data['pst_code_id']
    query.pst_notes = data['pst_notes']
    query.pst_recoveries = data['pst_recoveries']
    query.pst_error_type = data['pst_error_type']
    query.pst_coded_by_id = data['pst_coded_by_id']
    query.pst_signed_off_by_id = data['pst_signed_off_by_id']
    query.apo_code_id = data['apo_code_id']
    query.apo_notes = data['apo_notes']
    query.apo_recoveries = data['apo_recoveries']
    query.apo_error_type = data['apo_error_type']
    query.apo_coded_by_id = data['apo_coded_by_id']
    query.apo_signed_off_by_id = data['apo_signed_off_by_id']

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# TODO: add endpoint for images



#
