'''
Project Endpoints
'''
import json
import pandas as pd
import random
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from functools import reduce
from src.models import *
from src.util import validate_request_data

projects = Blueprint('projects', __name__)
#===============================================================================
# Toggle Favourite for User
@projects.route('/toggle_favourite/<path:id>', methods=['PUT'])
@jwt_required
def toggle_favourite(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        query = UserProject.query
        query = query.filter_by(user_id=current_user.id)
        query = query.filter_by(project_id=id)
        query = query.first()
        query.is_favourite = not query.is_favourite
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response)

#===============================================================================
# GET ALL PROJECT
@projects.route('/', defaults={'id':None}, methods=['GET'])
@projects.route('/<path:id>', methods=['GET'])
# @jwt_required
def get_projects(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    try:
        query = Project.query

        # ID filter
        if id is not None:
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError('ID {} does not exist.'.format(id))
        # Set ORDER
        query = query.order_by('name')
        # Query on is_approved (is_approved, 1 or 0)
        query = query.filter_by(is_approved=bool(args['is_approved'])) if 'is_approved' in args.keys() and args['is_approved'].isdigit() else query
        # Query on is_completed (is_completed, 1 or 0)
        query = query.filter_by(is_completed=bool(args['is_completed'])) if 'is_completed' in args.keys() and args['is_completed'].isdigit() else query
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
    return jsonify(response)

#===============================================================================
# POST NEW PROJECT
@projects.route('/', methods=['POST'])
# @jwt_required
def post_project():
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
        # input validation
        request_types = {
            'name': 'str',
            'client_id': 'int',
            'project_users': 'list',
            'engagement_partner_id': 'int',
            'engagement_manager_id': 'int',
            'tax_scope': 'dict',
            'engagement_scope': 'dict'
        }
        validate_request_data(data, request_types)
        # scope key checking
        def scopecheck(typecheck, basedata, keys):
            for key in keys:
                if key not in basedata:
                    raise ValueError('Scope with key {} has not been supplied.'.format(key))
                if typecheck and not isinstance(basedata[key], bool):
                    raise ValueError('Scope with key {} has wrong data type.'.format(key))
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
            raise ValueError('Project {} already exist.'.format(data['name']))

        # client_id validation
        client = Client.find_by_id(data['client_id'])
        if not client:
            raise ValueError('Client id does not exist.'.format(data['client_id']))

        # engagement_partner_id validation
        eng_part = User.find_by_id(data['engagement_partner_id'])
        if not eng_part:
            raise ValueError('User id {} does not exist for engagement partner.'.format(data['engagement_partner_id']))

        # engagement_manager_id validation
        eng_mana = User.find_by_id(data['engagement_manager_id'])
        if not eng_mana:
            raise ValueError('User id {} does not exist for engagement manager.'.format(data['engagement_manager_id']))

        # BUILD transaction
        new_project = Project(
            name = data['name'],
            project_client = client,
            engagement_partner_user = eng_part,
            engagement_manager_user = eng_mana,

            has_ts_gst = data['tax_scope']['has_ts_gst'],
            has_ts_hst = data['tax_scope']['has_ts_hst'],
            has_ts_qst = data['tax_scope']['has_ts_qst'],
            has_ts_pst = data['tax_scope']['has_ts_pst'],
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
        for user_id in data['project_users']:
            user = User.find_by_id(user_id)
            if not user:
                raise ValueError('Added project user with id {} does not exist'.format(user_id))

        # Add user_projects from project_users
        for user_id in data['project_users']:
            user = User.find_by_id(user_id)
            new_user_project = UserProject(
                user_project_user = user,
                user_project_project = new_project,
            )
            db.session.add(new_user_project)

        db.session.commit()
        response['message'] = 'Created project {}'.format(data['name'])
        response['payload'] = [Project.find_by_id(new_project.id).serialize]
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
# APPLY PAREDOWN RULES TO A PROJECT (NOTE: INCOMPLETE; REQUIRES TRANS. DATA)
@projects.route('/<int:id>/apply_paredown/', methods=['POST'])
# @jwt_required
def apply_paredown_rules(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        query = Project.query

        # Check if project exists
        if id is not None:
            query = query.filter_by(id=id)
            if not query.first():
                raise ValueError('Project ID {} does not exist.'.format(id))

        # Retrieve and create the rule objects
        paredown_rule_entries = ParedownRule.query
        rules = []
        for pr in paredown_rule_entries:
            i = pr.id
            conds = ParedownRuleCondition.query.filter_by(paredown_rule_id=i).all()
            pcs = [ParedownConditionObject(*(p.field,p.operator,p.value)) for p in conds]
            rules.append(ParedownRuleObject(pcs, pr.code, pr.comment))

        # *** TBC: CREATE DATAFRAME df WITH APPROPRIATE TRANSACTION Data
        df = pd.DataFrame()

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
# UPDATE A PROJECT
@projects.route('/<path:id>', methods=['PUT'])
# @jwt_required
def update_project(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    data = request.get_json()

    try:
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
        # scope key checking
        def scopecheck(typecheck, basedata, keys):
            for key in keys:
                if key not in basedata:
                    raise ValueError('Scope with key {} has not been supplied.'.format(key))
                if typecheck and not isinstance(basedata[key], bool):
                    raise ValueError('Scope with key {} has wrong data type.'.format(key))
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
            raise ValueError('Project ID {} does not exist.'.format(id))

        # CHECK CONSTRAINTS: name
        check = Project.query.filter_by(name=data['name']).filter(Project.id != id).first()
        if check:
            raise ValueError('Project name {} already exist.'.format(data['name']))

        # update name
        query.name = data['name']
        # client_id validate and update
        client = Client.find_by_id(data['client_id'])
        if not client:
            raise ValueError('Client id does not exist')
        query.project_client = client
        # lock paredown update
        query.is_paredown_locked = data['is_paredown_locked']
        # archive project update
        query.is_completed = data['is_completed']
        # engagement_partner_id validation and update
        eng_part = User.find_by_id(data['engagement_partner_id'])
        if not eng_part:
            raise ValueError('User id does not exist for engagement partner.'.format(data['engagement_partner_id']))
        query.engagement_partner_user = eng_part
        # engagement_manager_id validation
        eng_mana = User.find_by_id(data['engagement_manager_id'])
        if not eng_mana:
            raise ValueError('User id does not exist for engagement manager.'.format(data['engagement_manager_id']))
        query.engagement_manager_user = eng_mana

        query.has_ts_gst = data['tax_scope']['has_ts_gst']
        query.has_ts_hst = data['tax_scope']['has_ts_hst']
        query.has_ts_qst = data['tax_scope']['has_ts_qst']
        query.has_ts_pst = data['tax_scope']['has_ts_pst']
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
        for user_id in data['project_users']:
            user = User.find_by_id(user_id)
            if not user:
                raise ValueError('Added project user with id {} does not exist'.format(user_id))

        # Add user_projects from project_users
        user_projects = UserProject.query.filter_by(project_id=id).all()
        user_list = list(set(data['project_users']))
        for user_project in user_projects:
            if user_project.user_id in user_list:
                user_list.remove(user_project.user_id)
            else:
                db.session.delete(user_project)
        for user_id in user_list:
            user = User.find_by_id(user_id)
            new_user_project = UserProject(
                user_project_user = user,
                user_project_project = query,
            )
            db.session.add(new_user_project)

        db.session.commit()
        response['message'] = 'Updated project with id {}'.format(id)
        response['payload'] = [Project.find_by_id(id).serialize]
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response)

#===============================================================================
# DELETE A PROJECT
@projects.route('/<path:id>', methods=['DELETE'])
# @jwt_required
def delete_project(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    try:
        query = Project.query.filter_by(id=id).first()
        if not query:
            raise ValueError('Project ID {} does not exist.'.format(id))

        deletedproject = query.serialize
        db.session.delete(query)

        db.session.commit()
        response['message'] = 'Deleted project id {}'.format(deletedproject['id'])
        response['payload'] = [deletedproject]
    except ValueError as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 400
    except Exception as e:
        db.session.rollback()
        response = { 'status': 'error', 'message': str(e), 'payload': [] }
        return jsonify(response), 500
    return jsonify(response)

#===============================================================================
# HELPER CLASSES AND FUNCTIONS

# The class applies a paredown rule to project data
class ParedownRuleObject:

    def __init__(self, paredown_conditions, code, comment=None):
        self.paredown_conditions = paredown_conditions
        self.code = code
        self.comment = comment

    def apply_to_data(self, df):
        try:
            # Check if paredown columns exist
            if not all([col in df.columns for col in [pdc.field_name for pdc in self.paredown_conditions]]):
                raise ValueError("Cannot apply rule. DataFrame does not contain at least one required field_name.")

            fields_functions = [(pc.field_name,pc.value_type,pc.evaluator) for pc in self.paredown_conditions]
            return reduce(lambda x,y: x & y, [df[ff[0]].astype(ff[1]).apply(ff[2]) for ff in fields_functions])
        except Exception as e:
            raise Exception("Applying paredown rule failed: {}".format(str(e)))

# Class to create a valid paredown condition object
class ParedownConditionObject():

    def __init__(self, field_name, operator, value):

        self.field_name = field_name         #The data field name
        self.operator = operator            #The operator between
        self.value = value                  #The value that the data field is compared to
        if self.operator in ['>','<','==','>=','<=','!=']:
            self.value_type = 'float'
            lambda_func_str = 'lambda x : True if x {} {} else False'.format(self.operator, self.value)
        else:
            self.value_type = 'str'
            if self.operator == 'contains':
                lambda_func_str = 'lambda x : True if re.search(r\'\\b{}\\b\', x, re.IGNORECASE) else False'.format(self.value)
            else:
                lambda_func_str = 'lambda x : True if x {} {} else False'.format(self.operator, self.value)

        self.evaluator = eval(lambda_func_str)
