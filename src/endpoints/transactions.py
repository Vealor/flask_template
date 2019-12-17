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
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
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

    payload = {
        'data': [],
        'transaction_details': {}
    }
    for i in query.all():
        txn = i.serialize
        payload['data'].append({**txn[2], **{'id':txn[0]}})
        payload['transaction_details'][txn[0]] = txn[1]

    response['payload'] = payload

    return jsonify(response), 200

#===============================================================================
# Check if transaction locked
@transactions.route('/<int:id>/is_locked', methods=['GET'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
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
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
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
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
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
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def approve_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    # TODO: make sure user has access to the project
    #       make sure user has permission to approve

    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))
    if query.transaction_project.has_ts_gst_hst:
        if not query.gst_hst_signed_off_by_id:
            raise InputError('Transaction ID {} requires sign off on GST_HST codes before being approved.'.format(id))
    if query.transaction_project.has_ts_qst:
        if not query.qst_signed_off_by_id:
            raise InputError('Transaction ID {} requires sign off on QST codes before being approved.'.format(id))
    if query.transaction_project.has_ts_pst:
        if not query.pst_signed_off_by_id:
            raise InputError('Transaction ID {} requires sign off on PST codes before being approved.'.format(id))
    if query.transaction_project.has_ts_apo:
        if not query.apo_signed_off_by_id:
            raise InputError('Transaction ID {} requires sign off on APO codes before being approved.'.format(id))

    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is currently locked and not by you!'.format(id))
    if query.locked_user_id == current_user.id:
        raise InputError('Transaction ID {} is currently locked by you! Please unlock before approval.'.format(id))

    if query.approved_user_id == current_user.id:
        response['message'] = 'You have already approved this transaction!'
    else:
        query.approved_user_id = current_user.id
        query.modified = func.now()
        response['message'] = 'Transaction approved.'

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# BATCH Approve Transaction
@transactions.route('/batch/approve', methods=['PUT'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def batch_approve_transaction():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    if not isinstance(data, list):
        raise InputError("Input batch must be list of IDs")

    # TODO: make sure user has access to the project
    #       make sure user has permission to approve
    for id in data:
        query = Transaction.find_by_id(id)
        if not query:
            raise NotFoundError('Transaction ID {} does not exist.'.format(id))
        if query.transaction_project.has_ts_gst_hst:
            if not query.gst_hst_signed_off_by_id:
                raise InputError('Transaction ID {} requires sign off on GST_HST codes before being approved.'.format(id))
        if query.transaction_project.has_ts_qst:
            if not query.qst_signed_off_by_id:
                raise InputError('Transaction ID {} requires sign off on QST codes before being approved.'.format(id))
        if query.transaction_project.has_ts_pst:
            if not query.pst_signed_off_by_id:
                raise InputError('Transaction ID {} requires sign off on PST codes before being approved.'.format(id))
        if query.transaction_project.has_ts_apo:
            if not query.apo_signed_off_by_id:
                raise InputError('Transaction ID {} requires sign off on APO codes before being approved.'.format(id))

        if query.locked_transaction_user and query.locked_user_id != current_user.id:
            raise InputError('Transaction ID {} is currently locked and not by you!'.format(id))
        if query.locked_user_id == current_user.id:
            raise InputError('Transaction ID {} is currently locked by you! Please unlock before approval.'.format(id))

        query.approved_user_id = current_user.id
        query.modified = func.now()
        db.session.flush()

    response['message'] = 'Transactions approved.'

    db.session.commit()
    response['payload'] = []

    return jsonify(response), 200

#===============================================================================
# UnApprove Transaction
@transactions.route('/<int:id>/unapprove', methods=['PUT'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
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
        query.modified = func.now()
        response['message'] = 'Transaction unapproved.'

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# BATCH UnApprove Transaction
@transactions.route('/batch/unapprove', methods=['PUT'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def batch_unapprove_transaction():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()
    if not isinstance(data, list):
        raise InputError("Input batch must be list of IDs")

    # TODO: make sure user has access to the project
    #       make sure user has permission to unapprove
    for id in data:
        query = Transaction.find_by_id(id)
        if not query:
            raise NotFoundError('Transaction ID {} does not exist.'.format(id))
        if query.locked_transaction_user and query.locked_user_id != current_user.id:
            raise InputError('Transaction ID {} is currently locked and not by you!'.format(id))

        # TODO: check if use can even unapprove the given transaction
        query.approved_user_id = None
        query.modified = func.now()
        db.session.flush()

    response['message'] = 'Transaction unapproved.'

    db.session.commit()
    response['payload'] = []

    return jsonify(response), 200

#===============================================================================
# UPDATE A TRANSACTION information
@transactions.route('/<int:id>', methods=['PUT'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def update_transaction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # TODO: make sure user has access to the project
    request_types = {
        'gst_hst_codes': ['list','NoneType'],
        'gst_hst_notes_internal': ['str','NoneType'],
        'gst_hst_notes_external': ['str','NoneType'],
        'gst_hst_recoveries': ['float','NoneType'],
        'gst_hst_error_type': ['str','NoneType'],
        'gst_hst_coded_by_id': ['int','NoneType'],
        'gst_hst_signed_off_by_id': ['int','NoneType'],

        'qst_codes': ['list','NoneType'],
        'qst_notes_internal': ['str','NoneType'],
        'qst_notes_external': ['str','NoneType'],
        'qst_recoveries': ['float','NoneType'],
        'qst_error_type': ['str','NoneType'],
        'qst_coded_by_id': ['int','NoneType'],
        'qst_signed_off_by_id': ['int','NoneType'],

        'pst_codes': ['list','NoneType'],
        'pst_notes_internal': ['str','NoneType'],
        'pst_notes_external': ['str','NoneType'],
        'pst_recoveries': ['float','NoneType'],
        'pst_error_type': ['str','NoneType'],
        'pst_coded_by_id': ['int','NoneType'],
        'pst_signed_off_by_id': ['int','NoneType'],

        'apo_codes': ['list','NoneType'],
        'apo_notes_internal': ['str','NoneType'],
        'apo_notes_external': ['str','NoneType'],
        'apo_recoveries': ['float','NoneType'],
        'apo_error_type': ['str','NoneType'],
        'apo_coded_by_id': ['int','NoneType'],
        'apo_signed_off_by_id': ['int','NoneType']
    }
    validate_request_data(data, request_types)
    if len(data['gst_hst_notes_internal']) > 2048:
        raise InputError('GST_HST Internal Notes must be greater than 0 characters and no more than 2048')
    if len(data['gst_hst_notes_external']) > 2048:
        raise InputError('GST_HST External Notes must be greater than 0 characters and no more than 2048')
    if len(data['qst_notes_internal']) > 2048:
        raise InputError('QST Internal Notes must be greater than 0 characters and no more than 2048')
    if len(data['qst_notes_external']) > 2048:
        raise InputError('QST External Notes must be greater than 0 characters and no more than 2048')
    if len(data['pst_notes_internal']) > 2048:
        raise InputError('PST Internal Notes must be greater than 0 characters and no more than 2048')
    if len(data['pst_notes_external']) > 2048:
        raise InputError('PST External Notes must be greater than 0 characters and no more than 2048')
    if len(data['apo_notes_internal']) > 2048:
        raise InputError('APO Internal Notes must be greater than 0 characters and no more than 2048')
    if len(data['apo_notes_external']) > 2048:
        raise InputError('APO External Notes must be greater than 0 characters and no more than 2048')

    # UPDATE user
    query = Transaction.find_by_id(id)
    if not query:
        raise NotFoundError('Transaction ID {} does not exist.'.format(id))

    if query.locked_transaction_user and query.locked_user_id != current_user.id:
        raise InputError('Transaction ID {} is locked and not by you!'.format(id))
    if not query.locked_user_id:
        raise InputError('Please lock transaction ID {} before updating!'.format(id))

    if (data['gst_hst_coded_by_id'] == data['gst_hst_signed_off_by_id']
        or data['qst_coded_by_id'] == data['qst_signed_off_by_id']
        or data['pst_coded_by_id'] == data['pst_signed_off_by_id']
        or data['apo_coded_by_id'] == data['apo_signed_off_by_id']
    ):
        raise InputError('You can not code and sign off the same transaction tax type!')

    ### GST HST
    query.update_codes(list(set(data['gst_hst_codes'])), 'gst_hst')
    query.gst_hst_notes_internal = data['gst_hst_notes_internal']
    query.gst_hst_notes_external = data['gst_hst_notes_external']
    query.gst_hst_recoveries = data['gst_hst_recoveries']
    query.gst_hst_error_type = data['gst_hst_error_type']
    query.gst_hst_coded_by_id = data['gst_hst_coded_by_id']
    query.gst_hst_signed_off_by_id = data['gst_hst_signed_off_by_id']


    ### QST
    query.update_codes(list(set(data['qst_codes'])), 'qst')
    query.qst_notes_internal = data['qst_notes_internal']
    query.qst_notes_external = data['qst_notes_external']
    query.qst_recoveries = data['qst_recoveries']
    query.qst_error_type = data['qst_error_type']
    query.qst_coded_by_id = data['qst_coded_by_id']
    query.qst_signed_off_by_id = data['qst_signed_off_by_id']

    ### PST
    query.update_codes(list(set(data['pst_codes'])), 'pst')
    query.pst_notes_internal = data['pst_notes_internal']
    query.pst_notes_external = data['pst_notes_external']
    query.pst_recoveries = data['pst_recoveries']
    query.pst_error_type = data['pst_error_type']
    query.pst_coded_by_id = data['pst_coded_by_id']
    query.pst_signed_off_by_id = data['pst_signed_off_by_id']

    ### APO
    query.update_codes(list(set(data['apo_codes'])), 'apo')
    query.apo_notes_internal = data['apo_notes_internal']
    query.apo_notes_external = data['apo_notes_external']
    query.apo_recoveries = data['apo_recoveries']
    query.apo_error_type = data['apo_error_type']
    query.apo_coded_by_id = data['apo_coded_by_id']
    query.apo_signed_off_by_id = data['apo_signed_off_by_id']

    query.modified = func.now()

    # TODO: ADD MODIFIED DATETIME

    db.session.commit()
    response['payload'] = [Transaction.find_by_id(id).serialize]

    return jsonify(response), 200

#===============================================================================
# TODO: add endpoint for images



#
