'''
Project Endpoints
'''
import json
import multiprocessing as mp
import pandas as pd
import random
import re
import src.prediction.model_client as cm
import src.prediction.model_master as mm
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from functools import reduce
from src.errors import *
from src.models import *
from src.offload.apply_paredown import *
from src.prediction.preprocessing import preprocess_data, transactions_to_dataframe
from src.util import validate_request_data
from src.wrappers import has_permission, exception_wrapper

projects = Blueprint('projects', __name__)
#===============================================================================
# Toggle Favourite for User
@projects.route('/<int:id>/toggle_favourite', methods=['PUT'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def toggle_favourite(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = UserProject.query.filter_by(user_id=current_user.id)
    query = query.filter_by(project_id=id).first()
    if not query:
        raise NotFoundError("This project can not be toggled as a favourite or does not exist.")
    query.is_favourite = not query.is_favourite
    db.session.commit()

    return jsonify(response)

#===============================================================================
# GET ALL PROJECT
@projects.route('/', defaults={'id':None}, methods=['GET'])
@projects.route('/<int:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_projects(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = Project.query
    # ID filter
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('ProjectID {} does not exist.'.format(id))
    # Set ORDER
    query = query.order_by('name')
    # Query on is_approved (is_approved, 1 or 0)
    query = query.filter_by(is_approved=bool(args['is_approved'])) if 'is_approved' in args.keys() and args['is_approved'].isdigit() else query
    # Query on is_completed (is_completed, 1 or 0)
    query = query.filter_by(is_completed=bool(args['is_completed'])) if 'is_completed' in args.keys() and args['is_completed'].isdigit() else query
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response)

#===============================================================================
# GET ALL Predictive Calculations
@projects.route('/<int:id>/predictive_calculations', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_predictive_calculations(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = Project.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('Project ID {} does not exist.'.format(id))
    if 'vendor_num' not in args.keys():
        raise InputError('Please specify a vendor_num as an argument for the query.')

    green_pst_but_no_qst = None
    yellow_pst_but_no_qst = None

    average_number = engine.execute("""select AVG(cast(data ->> 'eff_rate' as float))
                from transactions as R
                where cast(data ->> 'vend_num' as text) = '{vend_num}'
                and project_id = {project_id}
                and data ->> 'transaction_attributes' NOT LIKE '%NoITC%';
                """)

    transaction_set = Transaction.query.filter_by(project_id=id)
    transaction_set = transaction_set.filter(Transaction.data['vend_num'].astext == args['vendor_num']).all()

    for txn in transaction_set:
        # do calculations
        pass



    response['payload'] = {
        'green_pst_but_no_qst': green_pst_but_no_qst,
        'yellow_pst_but_no_qst': yellow_pst_but_no_qst,
    }

    return jsonify(response)

#===============================================================================
# POST NEW PROJECT
@projects.route('/', methods=['POST'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def post_project():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # input validation
    request_types = {
        'name': ['str'],
        'client_id': ['int'],
        'project_users': ['list'],
        'lead_partner_id': ['int'],
        'lead_manager_id': ['int'],
        'tax_scope': ['dict'],
        'engagement_scope': ['dict']
    }
    validate_request_data(data, request_types)
    # scope key checking
    def scopecheck(typecheck, basedata, keys):
        for key in keys:
            if key not in basedata:
                raise InputError('Scope with key {} has not been supplied.'.format(key))
            if typecheck and not isinstance(basedata[key], bool):
                raise InputError('Scope with key {} has wrong data type.'.format(key))
    scopecheck(False, data, ['tax_scope', 'engagement_scope'])
    scopecheck(True, data['tax_scope'], ['has_ts_gst','has_ts_hst','has_ts_qst','has_ts_pst','has_ts_vat','has_ts_mft','has_ts_ct','has_ts_excise','has_ts_customs','has_ts_crown','has_ts_freehold'])
    scopecheck(False, data['engagement_scope'], ['indirect_tax','accounts_payable','customs','royalties','data'])
    scopecheck(True, data['engagement_scope']['indirect_tax'], ['has_es_caps','has_es_taxreturn','has_es_flowthrough','has_es_employeeexpense','has_es_pccards','has_es_coupons','has_es_creditnotes','has_es_edi','has_es_cars'])
    scopecheck(True, data['engagement_scope']['accounts_payable'], ['has_es_duplpay','has_es_unapplcredit','has_es_missedearly','has_es_otheroverpay'])
    scopecheck(True, data['engagement_scope']['customs'], ['has_es_firmanalysis','has_es_brokeranalysis'])
    scopecheck(True, data['engagement_scope']['royalties'], ['has_es_crowngca','has_es_crownalloc','has_es_crownincent','has_es_lornri','has_es_lorsliding','has_es_lordeduct','has_es_lorunder','has_es_lormissed'])
    scopecheck(True, data['engagement_scope']['data'], ['has_es_gstreg','has_es_cvm','has_es_taxgl','has_es_aps','has_es_ars','has_es_fxrates','has_es_trt','has_es_daf'])

    # CHECK CONSTRAINTS: name
    check = Project.query.filter_by(name=data['name']).first()
    if check:
        raise InputError('Project {} already exists.'.format(data['name']))

    # client_id validation
    client = Client.find_by_id(data['client_id'])
    if not client:
        raise InputError('Client id does not exist.'.format(data['client_id']))

    # lead_partner_id validation
    lead_part = User.find_by_id(data['lead_partner_id'])
    if not lead_part:
        raise InputError('User id {} does not exist for engagement partner.'.format(data['lead_partner_id']))

    # lead_manager_id validation
    lead_mana = User.find_by_id(data['lead_manager_id'])
    if not lead_mana:
        raise InputError('User id {} does not exist for engagement manager.'.format(data['lead_manager_id']))

    # BUILD transaction
    new_project = Project(
        name = data['name'],
        project_client = client,
        lead_partner_user = lead_part,
        lead_manager_user = lead_mana,

        has_ts_gst = data['tax_scope']['has_ts_gst'],
        has_ts_hst = data['tax_scope']['has_ts_hst'],
        has_ts_qst = data['tax_scope']['has_ts_qst'],
        has_ts_pst = data['tax_scope']['has_ts_pst'],
        has_ts_apo = data['tax_scope']['has_ts_apo'],
        has_ts_vat = data['tax_scope']['has_ts_vat'],
        has_ts_mft = data['tax_scope']['has_ts_mft'],
        has_ts_ct = data['tax_scope']['has_ts_ct'],
        has_ts_excise = data['tax_scope']['has_ts_excise'],
        has_ts_customs = data['tax_scope']['has_ts_customs'],
        has_ts_crown = data['tax_scope']['has_ts_crown'],
        has_ts_freehold = data['tax_scope']['has_ts_freehold'],

        has_es_caps = data['engagement_scope']['indirect_tax']['has_es_caps'],
        has_es_taxreturn = data['engagement_scope']['indirect_tax']['has_es_taxreturn'],
        has_es_flowthrough = data['engagement_scope']['indirect_tax']['has_es_flowthrough'],
        has_es_employeeexpense = data['engagement_scope']['indirect_tax']['has_es_employeeexpense'],
        has_es_pccards = data['engagement_scope']['indirect_tax']['has_es_pccards'],
        has_es_coupons = data['engagement_scope']['indirect_tax']['has_es_coupons'],
        has_es_creditnotes = data['engagement_scope']['indirect_tax']['has_es_creditnotes'],
        has_es_edi = data['engagement_scope']['indirect_tax']['has_es_edi'],
        has_es_cars = data['engagement_scope']['indirect_tax']['has_es_cars'],
        has_es_duplpay = data['engagement_scope']['accounts_payable']['has_es_duplpay'],
        has_es_unapplcredit = data['engagement_scope']['accounts_payable']['has_es_unapplcredit'],
        has_es_missedearly = data['engagement_scope']['accounts_payable']['has_es_missedearly'],
        has_es_otheroverpay = data['engagement_scope']['accounts_payable']['has_es_otheroverpay'],
        has_es_firmanalysis = data['engagement_scope']['customs']['has_es_firmanalysis'],
        has_es_brokeranalysis = data['engagement_scope']['customs']['has_es_brokeranalysis'],
        has_es_crowngca = data['engagement_scope']['royalties']['has_es_crowngca'],
        has_es_crownalloc = data['engagement_scope']['royalties']['has_es_crownalloc'],
        has_es_crownincent = data['engagement_scope']['royalties']['has_es_crownincent'],
        has_es_lornri = data['engagement_scope']['royalties']['has_es_lornri'],
        has_es_lorsliding = data['engagement_scope']['royalties']['has_es_lorsliding'],
        has_es_lordeduct = data['engagement_scope']['royalties']['has_es_lordeduct'],
        has_es_lorunder = data['engagement_scope']['royalties']['has_es_lorunder'],
        has_es_lormissed = data['engagement_scope']['royalties']['has_es_lormissed'],
        has_es_gstreg = data['engagement_scope']['data']['has_es_gstreg'],
        has_es_cvm = data['engagement_scope']['data']['has_es_cvm'],
        has_es_taxgl = data['engagement_scope']['data']['has_es_taxgl'],
        has_es_aps = data['engagement_scope']['data']['has_es_aps'],
        has_es_ars = data['engagement_scope']['data']['has_es_ars'],
        has_es_fxrates = data['engagement_scope']['data']['has_es_fxrates'],
        has_es_trt = data['engagement_scope']['data']['has_es_trt'],
        has_es_daf = data['engagement_scope']['data']['has_es_daf'],
    )
    # INSERT transaction
    db.session.add(new_project)
    db.session.flush()

    # project_users validation
    user_set = list(set(data['project_users'] + [data['lead_manager_id']] + [data['lead_partner_id']]))
    for user_id in user_set:
        user = User.find_by_id(user_id)
        if not user:
            raise InputError('Added project user with id {} does not exist'.format(user_id))

    # Add user_projects from project_users
    for user_id in user_set:
        user = User.find_by_id(user_id)
        new_user_project = UserProject(
            user_project_user = user,
            user_project_project = new_project,
        )
        db.session.add(new_user_project)
    db.session.flush()

    # Add all project parameters
    # TODO: ADD MORE PARAMS (JOHN)
    db.session.add(
        DataParam(
            project_id = new_project.id,
            process = 'aps_to_caps',
            param = 'potato',
            operator = Operator.equals,
            value = ['test', '123', '123.345'],
            is_many = True
        )
    )

    db.session.commit()
    response['message'] = 'Created project {}'.format(data['name'])
    response['payload'] = [Project.find_by_id(new_project.id).serialize]

    return jsonify(response), 201

#===============================================================================
# APPLY PAREDOWN RULES TO A PROJECT (NOTE: INCOMPLETE; REQUIRES TRANS. DATA)
@projects.route('/<int:id>/apply_paredown/', methods=['PUT'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def apply_paredown_rules(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    # GET BASE QUERY if exists
    query = Project.find_by_id(id)
    if not query:
        raise NotFoundError('Project ID {} does not exist.'.format(id))
    if query.is_paredown_locked:
        raise InputError('Paredown is Locked for Project with ID {}'.format(id))

    # get list of rules
    lobsecs = [i.lob_sector.name for i in query.project_client.client_client_entities]
    rules = []
    for i in ParedownRule.query.filter_by(is_active=True).all():
        if i.is_core and i.paredown_rule_approver1_id and i.paredown_rule_approver2_id:
            rules.append(i.serialize)
        elif i.lob_sectors:
            has_sec = False
            for l in i.lob_sectors:
                if l['code'] in lobsecs:
                    rules.append(i.serialize)
            if has_sec:
                rules.append(i.serialize)

    # apply rules to transactions
    # all transactions that aren't approved yet or locked
    txn_list = Transaction.query.filter_by(project_id=id).filter_by(approved_user_id=None).filter_by(locked_user_id=None).order_by("id").limit(50).all()
    # N = mp.cpu_count()
    # with mp.Pool(processes = N) as p:
    #     p.map(apply_rules_to_txn, [ {'rules': rules, 'txn_id': txn.id} for txn in txn_list])

    for txn in txn_list:
        print(txn.id)
        for rule in rules:
            # variable for checking conditions
            do_paredown = 0
            for condition in rule['conditions']:
                # print(condition)
                # ensure the field for the condition is in the data keys
                if condition['field'] in txn.data:

                    if condition['operator'] == 'contains':
                        # print("\tCONTAINS")
                        if re.search('(?<!\S)'+condition['value'].lower()+'(?!\S)', txn.data[condition['field']].lower()):
                            do_paredown +=1

                    elif condition['operator'] in ['>','<','==','>=','<=','!=']:
                        # print("\tLOGICAL OPERATOR")
                        proceed_operator = True

                        try:
                            value = float(condition['value'])
                            field = float(txn.data[condition['field']])
                        except ValueError as e:
                            # failed +=1
                            proceed_operator = False

                        if proceed_operator:
                            if condition['operator'] == '>' and field > value:
                                do_paredown +=1
                            elif condition['operator'] == '<' and field < value:
                                do_paredown +=1
                            elif condition['operator'] == '==' and field == value:
                                do_paredown +=1
                            elif condition['operator'] == '>=' and field >= value:
                                do_paredown +=1
                            elif condition['operator'] == '<=' and field <= value:
                                do_paredown +=1
                            elif condition['operator'] == '!=' and field != value:
                                do_paredown +=1
                        else:
                            print("Condition value or Transaction data field not fit for operator comparison.")
                    else:
                        raise Exception("Database issue for ParedownRuleCondition operator.")

            # if all conditions succeeded
            if do_paredown == len(rule['conditions']):
                # print("APPLY PAREDOWN TO TXN")
                if not txn.gst_signed_off_by_id:
                    txn.update_gst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.gst_codes] if txn.gst_codes else []))
                if not txn.hst_signed_off_by_id:
                    txn.update_hst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.hst_codes] if txn.hst_codes else []))
                if not txn.qst_signed_off_by_id:
                    txn.update_qst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.qst_codes] if txn.qst_codes else []))
                if not txn.pst_signed_off_by_id:
                    txn.update_pst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.pst_codes] if txn.pst_codes else []))
                if not txn.apo_signed_off_by_id:
                    txn.update_apo_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.apo_codes] if txn.apo_codes else []))

    db.session.commit()

    response['message'] = 'Applied paredown for Transactions in Project with id {}'.format(id)
    response['payload'] = []

    return jsonify(response), 200

#===============================================================================
# APPLY PREDICTION MODEL TO A PROJECT
#@projects.route('/<int:id>/apply_prediction/', methods=['PUT'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def apply_prediction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    request_types = {
        'use_client_model': ['bool'],
    }
    validate_request_data(data, request_types)

    # Get the data to predict
    project = Project.find_by_id(id)
    if not project:
        raise NotFoundError('Project with ID {} does not exist.'.format(id))
    project_transactions = Transaction.query.filter_by(project_id = id).filter(Transaction.approved_user_id == None)
    if project_transactions.count() == 0:
        raise ValueError('Project has no transactions to predict.')

    print("Create model.")
    # Get the appropriate active model, create the model object and alter transcation flags
    if data['use_client_model']:
        active_model = ClientModel.find_active_for_client(project.client_id)
        if not active_model:
            raise ValueError('No client model has been trained or is active for client ID {}.'.format(project.client_id))
        lh_model = cm.ClientPredictionModel(active_model.pickle)
        project_transactions.update({Transaction.master_model_id : None})
        project_transactions.update({Transaction.client_model_id :active_model.id})
    else:
        active_model = MasterModel.find_active()
        if not active_model:
            raise ValueError('No master model has been trained or is active.')
        lh_model = mm.MasterPredictionModel(active_model.pickle)
        project_transactions.update({Transaction.client_model_id : None})
        project_transactions.update({Transaction.master_model_id :active_model.id})

    predictors = active_model.hyper_p['predictors']


    # TODO: fix separation of data so that prediction happens on transactions with IDs
    # Can't assume that final zip lines up arrays properly
    print("Pull transactions to df.")
    df_predict = transactions_to_dataframe(project_transactions)
    print("Preprocessing...")
    df_predict = preprocess_data(df_predict, preprocess_for='prediction',predictors=predictors)

    # Get probability of each transaction being class '1'
    probability_recoverable = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]

    project_transactions.update({Transaction.is_predicted : True})
    for tr,pr in zip(project_transactions, probability_recoverable):
        tr.recovery_probability = pr

    db.session.commit()
    response['message'] = 'Prediction successful. Transactions have been marked.'
    return jsonify(response), 201
#===============================================================================
# APPLY PREDICTION MODEL TO A PROJECT
import numpy as np
@projects.route('/<int:id>/apply_prediction/', methods=['PUT'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def apply_dummy_prediction(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    request_types = {
        'use_client_model': ['bool'],
    }
    validate_request_data(data, request_types)

    # Get the data to predict
    project = Project.find_by_id(id)
    if not project:
        raise NotFoundError('Project with ID {} does not exist.'.format(id))

    #####################################
    #FOR DEMO
    trans_ids = list(range(1,45)) + [46] + [49,50]
    probability_recoverable = [x/100 for x in [10,80,80,80,90,80,75,10,80,80,80,80,65,85,80,60,80,80,80,80,60,80,15,75,10,75,75,75,75,75,75,75,75,60,85,80,80,10,75,70,55,10,10,55, 10, 5, 5]]

    ######################################

    project_transactions = Transaction.query.filter_by(project_id = id).filter(Transaction.id.in_(trans_ids))
    if project_transactions.count() == 0:
        raise ValueError('Project has no transactions to predict.')

    # Get the appropriate active model, create the model object and alter transcation flags
    if data['use_client_model']:
        active_model = ClientModel.find_active_for_client(project.client_id)
        if not active_model:
            raise ValueError('No client model has been trained or is active for client ID {}.'.format(project.client_id))
        lh_model = cm.ClientPredictionModel(active_model.pickle)
        project_transactions.update({Transaction.master_model_id : None})
        project_transactions.update({Transaction.client_model_id :active_model.id})
    else:
        active_model = MasterModel.find_active()
        if not active_model:
            raise ValueError('No master model has been trained or is active.')
        lh_model = mm.MasterPredictionModel(active_model.pickle)
        project_transactions.update({Transaction.client_model_id : None},synchronize_session="fetch")
        project_transactions.update({Transaction.master_model_id :active_model.id},synchronize_session="fetch")

    predictors = active_model.hyper_p['predictors']


    ## TODO: fix separation of data so that prediction happens on transactions with IDs
    ## Can't assume that final zip lines up arrays properly
    #df_predict = transactions_to_dataframe(project_transactions)
    #df_predict = preprocess_data(df_predict, preprocess_for='prediction',predictors=predictors)

    ## Get probability of each transaction being class '1'
    #probability_recoverable = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]


    project_transactions.update({Transaction.is_predicted : True}, synchronize_session="fetch")
    for tr,pr in zip(project_transactions, probability_recoverable):
        tr.recovery_probability = pr
        #tr.is_recoverable = True

    print("HERE!")
    db.session.commit()
    response['message'] = 'Prediction successful. Transactions have been marked.'
    return jsonify(response), 201

#===============================================================================
# UPDATE A PROJECT
@projects.route('/<int:id>', methods=['PUT'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def update_project(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    # input validation
    request_types = {
        'name': ['str'],
        'is_paredown_locked': ['bool'],
        'is_completed': ['bool'],
        'client_id': ['int'],
        'project_users': ['list'],
        'lead_partner_id': ['int'],
        'lead_manager_id': ['int'],
        'tax_scope': ['dict'],
        'engagement_scope': ['dict']
    }
    validate_request_data(data, request_types)
    # scope key checking
    def scopecheck(typecheck, basedata, keys):
        for key in keys:
            if key not in basedata:
                raise InputError('Scope with key {} has not been supplied.'.format(key))
            if typecheck and not isinstance(basedata[key], bool):
                raise InputError('Scope with key {} has wrong data type.'.format(key))
    scopecheck(False, data, ['tax_scope', 'engagement_scope'])
    scopecheck(True, data['tax_scope'], ['has_ts_gst','has_ts_hst','has_ts_qst','has_ts_pst','has_ts_vat','has_ts_mft','has_ts_ct','has_ts_excise','has_ts_customs','has_ts_crown','has_ts_freehold'])
    scopecheck(False, data['engagement_scope'], ['indirect_tax','accounts_payable','customs','royalties','data'])
    scopecheck(True, data['engagement_scope']['indirect_tax'], ['has_es_caps','has_es_taxreturn','has_es_flowthrough','has_es_employeeexpense','has_es_pccards','has_es_coupons','has_es_creditnotes','has_es_edi','has_es_cars'])
    scopecheck(True, data['engagement_scope']['accounts_payable'], ['has_es_duplpay','has_es_unapplcredit','has_es_missedearly','has_es_otheroverpay'])
    scopecheck(True, data['engagement_scope']['customs'], ['has_es_firmanalysis','has_es_brokeranalysis'])
    scopecheck(True, data['engagement_scope']['royalties'], ['has_es_crowngca','has_es_crownalloc','has_es_crownincent','has_es_lornri','has_es_lorsliding','has_es_lordeduct','has_es_lorunder','has_es_lormissed'])
    scopecheck(True, data['engagement_scope']['data'], ['has_es_gstreg','has_es_cvm','has_es_taxgl','has_es_aps','has_es_ars','has_es_fxrates','has_es_trt','has_es_daf'])

    # GET BASE QUERY if exists
    query = Project.find_by_id(id)
    if not query:
        raise NotFoundError('Project ID {} does not exist.'.format(id))

    # CHECK CONSTRAINTS: name
    check = Project.query.filter_by(name=data['name']).filter(Project.id != id).first()
    if check:
        raise InputError('Project name {} already exist.'.format(data['name']))

    # update name
    query.name = data['name']
    # client_id validate and update
    client = Client.find_by_id(data['client_id'])
    if not client:
        raise InputError('Client id does not exist')
    query.project_client = client
    # lock paredown update
    query.is_paredown_locked = data['is_paredown_locked']
    # archive project update
    query.is_completed = data['is_completed']
    # lead_partner_id validation and update
    lead_part = User.find_by_id(data['lead_partner_id'])
    if not lead_part:
        raise InputError('User id does not exist for engagement partner.'.format(data['lead_partner_id']))
    query.lead_partner_user = lead_part
    # lead_manager_id validation
    lead_mana = User.find_by_id(data['lead_manager_id'])
    if not lead_mana:
        raise InputError('User id does not exist for engagement manager.'.format(data['lead_manager_id']))
    query.lead_manager_user = lead_mana

    query.has_ts_gst = data['tax_scope']['has_ts_gst']
    query.has_ts_hst = data['tax_scope']['has_ts_hst']
    query.has_ts_qst = data['tax_scope']['has_ts_qst']
    query.has_ts_pst = data['tax_scope']['has_ts_pst']
    query.has_ts_apo = data['tax_scope']['has_ts_apo']
    query.has_ts_vat = data['tax_scope']['has_ts_vat']
    query.has_ts_mft = data['tax_scope']['has_ts_mft']
    query.has_ts_ct = data['tax_scope']['has_ts_ct']
    query.has_ts_excise = data['tax_scope']['has_ts_excise']
    query.has_ts_customs = data['tax_scope']['has_ts_customs']
    query.has_ts_crown = data['tax_scope']['has_ts_crown']
    query.has_ts_freehold = data['tax_scope']['has_ts_freehold']

    query.has_es_caps = data['engagement_scope']['indirect_tax']['has_es_caps']
    query.has_es_taxreturn = data['engagement_scope']['indirect_tax']['has_es_taxreturn']
    query.has_es_flowthrough = data['engagement_scope']['indirect_tax']['has_es_flowthrough']
    query.has_es_employeeexpense = data['engagement_scope']['indirect_tax']['has_es_employeeexpense']
    query.has_es_pccards = data['engagement_scope']['indirect_tax']['has_es_pccards']
    query.has_es_coupons = data['engagement_scope']['indirect_tax']['has_es_coupons']
    query.has_es_creditnotes = data['engagement_scope']['indirect_tax']['has_es_creditnotes']
    query.has_es_edi = data['engagement_scope']['indirect_tax']['has_es_edi']
    query.has_es_cars = data['engagement_scope']['indirect_tax']['has_es_cars']
    query.has_es_duplpay = data['engagement_scope']['accounts_payable']['has_es_duplpay']
    query.has_es_unapplcredit = data['engagement_scope']['accounts_payable']['has_es_unapplcredit']
    query.has_es_missedearly = data['engagement_scope']['accounts_payable']['has_es_missedearly']
    query.has_es_otheroverpay = data['engagement_scope']['accounts_payable']['has_es_otheroverpay']
    query.has_es_firmanalysis = data['engagement_scope']['customs']['has_es_firmanalysis']
    query.has_es_brokeranalysis = data['engagement_scope']['customs']['has_es_brokeranalysis']
    query.has_es_crowngca = data['engagement_scope']['royalties']['has_es_crowngca']
    query.has_es_crownalloc = data['engagement_scope']['royalties']['has_es_crownalloc']
    query.has_es_crownincent = data['engagement_scope']['royalties']['has_es_crownincent']
    query.has_es_lornri = data['engagement_scope']['royalties']['has_es_lornri']
    query.has_es_lorsliding = data['engagement_scope']['royalties']['has_es_lorsliding']
    query.has_es_lordeduct = data['engagement_scope']['royalties']['has_es_lordeduct']
    query.has_es_lorunder = data['engagement_scope']['royalties']['has_es_lorunder']
    query.has_es_lormissed = data['engagement_scope']['royalties']['has_es_lormissed']
    query.has_es_gstreg = data['engagement_scope']['data']['has_es_gstreg']
    query.has_es_cvm = data['engagement_scope']['data']['has_es_cvm']
    query.has_es_taxgl = data['engagement_scope']['data']['has_es_taxgl']
    query.has_es_aps = data['engagement_scope']['data']['has_es_aps']
    query.has_es_ars = data['engagement_scope']['data']['has_es_ars']
    query.has_es_fxrates = data['engagement_scope']['data']['has_es_fxrates']
    query.has_es_trt = data['engagement_scope']['data']['has_es_trt']
    query.has_es_daf = data['engagement_scope']['data']['has_es_daf']

    # project_users update
    user_set = list(set(data['project_users'] + [data['lead_manager_id']] + [data['lead_partner_id']]))
    for user_id in user_set:
        user = User.find_by_id(user_id)
        if not user:
            raise InputError('Added project user with id {} does not exist'.format(user_id))

    # Add user_projects from project_users
    user_projects = UserProject.query.filter_by(project_id=id).all()
    for user_project in user_projects:
        if user_project.user_id in user_set:
            user_set.remove(user_project.user_id)
        else:
            db.session.delete(user_project)
    for user_id in user_set:
        user = User.find_by_id(user_id)
        new_user_project = UserProject(
            user_project_user = user,
            user_project_project = query,
        )
        db.session.add(new_user_project)

    db.session.commit()
    response['message'] = 'Updated project with id {}'.format(id)
    response['payload'] = [Project.find_by_id(id).serialize]

    return jsonify(response)

#===============================================================================
# DELETE A PROJECT
@projects.route('/<int:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def delete_project(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = Project.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('Project ID {} does not exist.'.format(id))

    deletedproject = query.serialize
    db.session.delete(query)

    db.session.commit()
    response['message'] = 'Deleted project id {}'.format(deletedproject['id'])
    response['payload'] = [deletedproject]

    return jsonify(response)
