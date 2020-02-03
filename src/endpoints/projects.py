'''
Project Endpoints
'''
import re
import src.prediction.model_client as cm
import src.prediction.model_master as mm
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from src.errors import InputError, NotFoundError
from src.models import db, Client, ClientEntity, ClientModel, DataParam, MasterModel, Operator, ParedownRule, Project, Transaction, User, UserProject
from src.prediction.preprocessing import preprocess_data, transactions_to_dataframe
from src.util import validate_request_data, create_log
from src.wrappers import has_permission, exception_wrapper

projects = Blueprint('projects', __name__)
#===============================================================================
# Toggle Favourite for User
@projects.route('/<int:id>/toggle_favourite', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def toggle_favourite(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

    query = UserProject.query.filter_by(user_id=current_user.id)
    query = query.filter_by(project_id=id).first()
    if not query:
        raise NotFoundError("This project can not be toggled as a favourite or does not exist.")
    query.is_favourite = not query.is_favourite
    db.session.commit()

    return jsonify(response)

#===============================================================================
# GET ALL PROJECT
@projects.route('/', defaults={'id': None}, methods=['GET'])
@projects.route('/<int:id>', methods=['GET'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_projects(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
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
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_predictive_calculations(id):
    print('Checkpoint 1.0')
    args = request.args.to_dict()
    # helper function to calculate recovery value and volume for step 1
    def calculate_tax(province, prediction_strength_lower=0, prediction_strength_upper=1):
        jurisdiction_dict = {
            'gst': ['ab', 'nt', 'yt', 'nu'],
            'gst_pst': ['bc', 'sk','mb'],
            'gst_qst': ['qc'],
            'hst': ['nb', 'ns', 'on', 'nl', 'pe']
        }
        # TODO: only calculate for exceptions
        #  if province in jurisdiction_dict['gst'] ]  or in jurisdiction_dict['gst_pst'] for provinces in jurisdictions
        engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
        results = engine.execute("""SELECT COALESCE(SUM(CAST(data->>'ap_amt' AS FLOAT)), 0),
                               COALESCE(SUM(CAST(data->>'gst_hst' AS FLOAT)), 0),
                                COUNT(id)
                                FROM transactions
                                WHERE project_id = {project_id}
                                AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                                """.format(project_id=id, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
        ap_amt_sum, itc_claimed, tx_num = results[0], results[1], results[2]
        if province in jurisdiction_dict['gst']:
            total_value = (-1 * ap_amt_sum) * 5 / 105 - itc_claimed
        elif province in jurisdiction_dict['gst_pst']:
            gst_results = engine.execute("""SELECT COALESCE(SUM(CAST(data->>'ap_amt' AS FLOAT)), 0),
                            COALESCE(SUM(CAST(data->>'pst_sa' AS FLOAT)), 0),
                            COALESCE(COUNT(id), 0)
                            FROM transactions
                            WHERE project_id = {project_id}
                            AND CAST(data->>'pst_sa' AS FLOAT) > 0
                            AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                            """.format(project_id=id, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
            ap_amt_sum, pst_sa_sum, none_zero_tx_num = gst_results[0], gst_results[1], gst_results[2]
            pst_results = engine.execute("""SELECT COALESCE(SUM(CAST(data->>'ap_amt' AS FLOAT)), 0),
                            COALESCE(COUNT(id), 0)
                            FROM transactions
                            WHERE project_id = {project_id}
                            AND CAST(data->>'pst_sa' AS FLOAT) = 0
                            AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                            """.format(project_id=id, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
            zero_pst_amt_sum, zero_pst_tx_num = pst_results[0], pst_results[1]
            total_value = (-1 * ap_amt_sum + -1 * zero_pst_amt_sum) * 5 / 112 - itc_claimed + pst_sa_sum + (-1 * zero_pst_amt_sum * 7 / 112)
            tx_num = none_zero_tx_num + zero_pst_tx_num
        elif province in jurisdiction_dict['gst_qst']:
            qst_results = engine.execute("""SELECT COALESCE(SUM(CAST(data->>'qst' AS FLOAT)), 0)
                            FROM transactions
                            WHERE project_id = {project_id}
                            AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                            """.format(project_id=id, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
            qst_claimed = qst_results[0]
            gst_value = (-1 * ap_amt_sum) * 5 / 114.975 - itc_claimed
            qst_value = (-1 * ap_amt_sum) * 9.975 / 114.975 - qst_claimed
            total_value = gst_value + qst_value
        elif province  in jurisdiction_dict['hst']:
            total_value = (-1 * ap_amt_sum) * 13 / 113 - itc_claimed
        else:
            raise InputError("No matching jurisdiction rule found for:{ }".format(province))
        return total_value, tx_num

    def  check_tax_scope(jurisdictions):
        scopes_dict = {
            'ab': 'gst',
            'nt': 'gst',
            'yt': 'gst',
            'nu': 'gst',
            'bc': 'gst_pst',
            'sk': 'gst_pst',
            'mb': 'gst_pst',
            'qc': 'gst_qst',
            'nb': 'hst',
            'ns': 'hst',
            'on': 'hst',
            'nl': 'hst',
            'pe': 'hst'
        }
        seen_jurisdiction = set()
        for jurisdiction in jurisdictions:
            seen_jurisdiction.add(scopes_dict[jurisdiction])
        # pst but no qst
        if ('gst' in seen_jurisdiction or 'hst' in seen_jurisdiction) and 'gst_pst' in seen_jurisdiction:
            return 1
        # qst but no pst
        elif ('gst' in seen_jurisdiction or 'hst' in seen_jurisdiction) and 'gst_qst' in seen_jurisdiction:
            return 2
        # qst and pst
        elif ('gst' in seen_jurisdiction or 'hst' in seen_jurisdiction) and 'gst_qst' in seen_jurisdiction and 'gst_pst' in seen_jurisdiction:
            return 3
        else:
            raise ValueError("Can not find matching tax scope based on jurisdictions provided")

    # TODO: error handling
    def calc_gst_hst_mat(vend_num, prediction_strength_lower, prediction_strength_upper):
        temp_session = db.create_scoped_session()
        query_result = temp_session.execute("""SELECT COALESCE(SUM(CAST(data->>'ap_amt' AS FLOAT)), 0),
                        COALESCE(SUM(CAST(data->>'gst_hst' AS FLOAT)), 0),
                        COUNT(id)
                        FROM transactions
                        WHERE project_id = {project_id}
                        AND query_reference_num IS NOT NULL
                        AND cast(data ->> 'vend_num' as text) = '{vend_num}'
                        AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                        """.format(project_id=id, vend_num=vend_num, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
        ap_amount, gst_hst_claimed, num_of_txn = query_result[0], query_result[1], query_result[2]
        query_result = temp_session.execute("""SELECT COALESCE(AVG(CAST(data->>'eff_rate' AS FLOAT)), 0)
                        FROM transactions
                        WHERE project_id = {project_id}
                        AND query_reference_num = {query_num}
                        AND cast(data ->> 'vend_num' as text) = '{vend_num}';
                        """.format(project_id=id, query_num=query_num, vend_num=vend_num)).first()
        avg_eff_rate = query_result[0]
        calc_result = (-1 * ap_amount) * avg_eff_rate - gst_hst_claimed
        temp_session.close()
        return calc_result, num_of_txn

    # TODO: error handling
    def calc_qst_mat(vend_num, prediction_strength_lower, prediction_strength_upper):
        temp_session = db.create_scoped_session()
        query_result = temp_session.execute("""SELECT COALESCE(SUM(CAST(data->>'ap_amt' AS FLOAT)), 0),
                    COALESCE(SUM(CAST(data->>'qst' AS FLOAT)), 0),
                    COUNT(id)
                    FROM transactions
                    WHERE project_id = {project_id}
                    AND query_reference_num = {query_num}
                    AND cast(data ->> 'vend_num' as text) = '{vend_num}'
                    AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                    """.format(project_id=id, vend_num=vend_num, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
        ap_amount, qst_claimed, num_of_txn = query_result[0], query_result[1], query_result[2]
        calc_result = ( -1 * ap_amount) * (9.975 / 114.975) - qst_claimed
        temp_session.close()
        return calc_result, num_of_txn

    # TODO: error handling
    def calc_pst_mat(vend_num, prediction_strength_lower, prediction_strength_upper):
        temp_session = db.create_scoped_session()
        query_result = temp_session.execute("""SELECT COALESCE(SUM(CAST(data->>'ap_amt' AS FLOAT)), 0),
                    COUNT(id)
                    FROM transactions
                    WHERE project_id = {project_id}
                    AND query_reference_num = {query_num}
                    AND cast(data ->> 'vend_num' as text) = '{vend_num}'
                    AND CAST(data->>'pst_sa' AS FLOAT) = 0
                    AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                    """.format(project_id=id, vend_num=vend_num, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
        ap_amount, pst_claimed, num_of_txn = query_result[0], query_result[1], query_result[2]
        calc_result = ( -1 * ap_amount) * (7 / 112)
        query_result = temp_session.execute("""SELECT COALESCE(SUM(CAST(data->>'pst_sa' AS FLOAT)), 0),
                COUNT(id)
                FROM transactions
                WHERE project_id = {project_id}
                AND query_reference_num = {query_num}
                AND cast(data ->> 'vend_num' as text) = '{vend_num}'
                AND CAST(data->>'pst_sa' AS FLOAT) > 0
                AND recovery_probability BETWEEN {lower_limit} AND {upper_limit};
                """.format(project_id=id, vend_num=vend_num, lower_limit=prediction_strength_lower, upper_limit=prediction_strength_upper)).first()
        pst_sa_sum, num_of_non_zero_pst_sa_txn = query_result[0], query_result[1]
        calc_result += pst_sa_sum
        num_of_txn += num_of_non_zero_pst_sa_txn
        temp_session.close()
        return calc_result, num_of_txn

    def multiple_jurisdiction_calc(jurisdictions, vend_num, prediction_strength_lower, prediction_strength_upper):
        tax_scope = check_tax_scope(jurisdictions)
        total_value, total_volume = 0
        # pst but no qst
        if tax_scope == 1:
            gst_hst_value, gst_hst_volume = calc_gst_hst_mat(vend_num,  prediction_strength_lower, prediction_strength_upper)
            pst_value, pst_volume =  calc_pst_mat(vend_num, prediction_strength_lower, prediction_strength_upper)
            total_value = gst_hst_value + pst_value
            total_volume = gst_hst_volume + pst_volume
        # qst but no pst
        elif tax_scope == 2:
            gst_hst_value, gst_hst_volume = calc_gst_hst_mat(vend_num, prediction_strength_lower, prediction_strength_upper)
            qst_value, qst_volume =  calc_qst_mat(vend_num, prediction_strength_lower, prediction_strength_upper)
            total_value = gst_hst_value + qst_value
            total_volume = gst_hst_volume + qst_volume
        # qst and pst
        elif tax_scope == 3:
            gst_hst_value, gst_hst_volume = calc_gst_hst_mat(vend_num, prediction_strength_lower, prediction_strength_upper)
            pst_value, pst_volume =  calc_pst_mat(vend_num, prediction_strength_lower, prediction_strength_upper)
            qst_value, qst_volume  =  calc_qst_mat(vend_num, prediction_strength_lower, prediction_strength_upper)
            total_value = gst_hst_value + qst_value + pst_value
            total_volume = gst_hst_volume + qst_volume + pst_volume
        return total_value, total_volume
    print('Checkpoint 2.0')
    response = {'status': 'ok', 'message': '', 'payload': []}
    query = Project.query.filter_by(id=id)
    print(args.keys())
    if not query.first():
        raise NotFoundError('Project ID {} does not exist.'.format(id))
    if 'vend_num' not in args.keys():
        raise InputError('Please specify a vend_num as an argument for the query.')
    print('Checkpoint 3.0')
    client_id = query.first().serialize['client_id']
    jurisdictions = ClientEntity.query.filter_by(client_id=client_id).first().serialize["jurisdictions"]
    if len(jurisdictions) == 1:
        province = jurisdictions[0]['code'].lower()
        recoveries_total_value, recoveries_tx_num = calculate_tax(province, prediction_strength_lower=0.9)
        uncategorized_total_value, uncategorized_tx_num = calculate_tax(province, prediction_strength_lower=0.7, prediction_strength_upper=0.8999)
        print('Checkpoint 3.1')
    else:
        provinces =[ jurisdiction['code'].lower() for jurisdiction in jurisdictions ]
        recoveries_total_value, recoveries_tx_num = multiple_jurisdiction_calc(provinces, vendor_num, prediction_strength_lower=0.9)
        uncategorized_total_value, uncategorized_tx_num = multiple_jurisdiction_calc(provinces, vendor_num, prediction_strength_lower=0.7, prediction_strength_upper=0.8999)
        print('Checkpoint 3.2')
    print('Checkpoint 4.0')
    response['payload'] = {
        "recoveries_value": recoveries_total_value,
        "recoveries_volume": recoveries_tx_num,
        "uncategorized_value": uncategorized_total_value,
        "uncategorized_volume": uncategorized_tx_num
    }
    #  engine.execute("""select data ->> 'ap_amout' as float))
    #             from transactions as R
    #             where cast(data ->> 'vend_num' as text) = '{vend_num}'
    #             and project_id = {project_id}
    #             and data ->> 'transaction_attributes' NOT LIKE '%NoITC%';
    #             """.format(project_id = project_id, vend_num = vend_num))

    # if len(jurisdiction) == 1:
    #     province = jurisdiction[0]
    #     ap_amount = 0
    #     itc_claimed = 0

    #     if province == "AB" or province == "NT" or province == "YT" or province  == "NU":
    #         gst_value = ap_amount * 5/105 - itc_claimed
    #     elif province == "BC" or province == "SK" or province == "MB":
    #         psg_value =
    #     elif province == "QC" :
    #     elif province == "NB" or province == "NS", or procince == "ON" or prvince == "PE":
    #     else:
    # TODO: for step 2
    # if 'vendor_num' not in args.keys():
    #     raise InputError('Please specify a vendor_num as an argument for the query.')

    # green_pst_but_no_qst = None
    # yellow_pst_but_no_qst = None

    # average_number = engine.execute("""select AVG(cast(data ->> 'eff_rate' as float))
    #             from transactions as R
    #             where cast(data ->> 'vend_num' as text) = '{vend_num}'
    #             and project_id = {project_id}
    #             and data ->> 'transaction_attributes' NOT LIKE '%NoITC%';
    #             """.format(project_id = project_id, vend_num = vend_num))

    # print(average_number)

    # engine.execute("""
    # select id, (cast(data ->> 'ap_amt' as float) * {average_number}) - cast(data ->> 'gst_hst' as float) from transactions
    # where data ->> 'ap_amt' is not null and id = {transaction_id};
    # """.format(transaction_id = transaction_id, average_number = average_number))

    # transaction_set = Transaction.query.filter_by(project_id=id)
    # transaction_set = transaction_set.filter(Transaction.data['vend_num'].astext == args['vendor_num']).all()

    # for txn in transaction_set:
    #     # do calculations
    #     pass

    # response['payload'] = {
    #     'green_pst_but_no_qst': green_pst_but_no_qst,
    #     'yellow_pst_but_no_qst': yellow_pst_but_no_qst,
    # }

    return jsonify(response)

#===============================================================================
# POST NEW PROJECT
@projects.route('/', methods=['POST'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def post_project():
    response = {'status': 'ok', 'message': '', 'payload': []}
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
    if len(data['name']) < 1 or len(data['name']) > 128:
        raise InputError('Name must be greater than 1 character and no more than 128')

    # scope key checking
    def scopecheck(typecheck, basedata, keys):
        for key in keys:
            if key not in basedata:
                raise InputError('Scope with key {} has not been supplied.'.format(key))
            if typecheck and not isinstance(basedata[key], bool):
                raise InputError('Scope with key {} has wrong data type.'.format(key))
    scopecheck(False, data, ['tax_scope', 'engagement_scope'])
    scopecheck(True, data['tax_scope'], ['has_ts_gst_hst', 'has_ts_qst', 'has_ts_pst', 'has_ts_vat', 'has_ts_mft', 'has_ts_ct', 'has_ts_excise', 'has_ts_customs', 'has_ts_crown', 'has_ts_freehold'])
    scopecheck(False, data['engagement_scope'], ['indirect_tax', 'accounts_payable', 'customs', 'royalties', 'data'])
    scopecheck(True, data['engagement_scope']['indirect_tax'], ['has_es_caps', 'has_es_taxreturn', 'has_es_flowthrough', 'has_es_employeeexpense', 'has_es_pccards', 'has_es_coupons', 'has_es_creditnotes', 'has_es_edi', 'has_es_cars'])
    scopecheck(True, data['engagement_scope']['accounts_payable'], ['has_es_duplpay', 'has_es_unapplcredit', 'has_es_missedearly', 'has_es_otheroverpay'])
    scopecheck(True, data['engagement_scope']['customs'], ['has_es_firmanalysis', 'has_es_brokeranalysis'])
    scopecheck(True, data['engagement_scope']['royalties'], ['has_es_crowngca', 'has_es_crownalloc', 'has_es_crownincent', 'has_es_lornri', 'has_es_lorsliding', 'has_es_lordeduct', 'has_es_lorunder', 'has_es_lormissed'])
    scopecheck(True, data['engagement_scope']['data'], ['has_es_gstreg', 'has_es_cvm', 'has_es_taxgl', 'has_es_aps', 'has_es_ars', 'has_es_fxrates', 'has_es_trt', 'has_es_daf'])

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

        has_ts_gst_hst = data['tax_scope']['has_ts_gst_hst'],
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
    create_log(current_user, 'create', 'User created Project', 'Name: ' + str(data['name']))

    return jsonify(response), 201

#===============================================================================
# APPLY PAREDOWN RULES TO A PROJECT (NOTE: INCOMPLETE; REQUIRES TRANS. DATA)
@projects.route('/<int:id>/apply_paredown/', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def apply_paredown_rules(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

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
    txn_list = Transaction.query.filter_by(project_id=id).filter_by(approved_user_id=None).filter_by(locked_user_id=None).order_by("id").limit(52).all()
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
                        print(r'(?<!\S)' + condition['value'].lower() + r'(?!\S)', txn.data[condition['field']].lower())
                        if re.search(r'(?<!\S)' + condition['value'].lower() + r'(?!\S)', txn.data[condition['field']].lower()):
                            do_paredown += 1

                    elif condition['operator'] in ['>', '<', '==', '>=', '<=', '!=']:
                        # print("\tLOGICAL OPERATOR")
                        proceed_operator = True

                        try:
                            value = float(condition['value'])
                            field = float(txn.data[condition['field']])
                        except ValueError:
                            proceed_operator = False

                        if proceed_operator:
                            if condition['operator'] == '>' and field > value:
                                do_paredown += 1
                            elif condition['operator'] == '<' and field < value:
                                do_paredown += 1
                            elif condition['operator'] == '==' and field == value:
                                do_paredown += 1
                            elif condition['operator'] == '>=' and field >= value:
                                do_paredown += 1
                            elif condition['operator'] == '<=' and field <= value:
                                do_paredown += 1
                            elif condition['operator'] == '!=' and field != value:
                                do_paredown += 1
                        else:
                            print("Condition value or Transaction data field not fit for operator comparison.")
                    else:
                        raise Exception("Database issue for ParedownRuleCondition operator {}".format(condition['operator']))

            # if all conditions succeeded
            if do_paredown == len(rule['conditions']):
                # print("APPLY PAREDOWN TO TXN")
                gst_hst_code_list = [c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'gst_hst'] if txn.transaction_codes else []
                qst_code_list = [c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'qst'] if txn.transaction_codes else []
                pst_code_list = [c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'pst'] if txn.transaction_codes else []
                apo_code_list = [c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'apo'] if txn.transaction_codes else []
                if not txn.gst_hst_signed_off_by_id:
                    if rule['code']['code_number'] not in gst_hst_code_list:
                        txn.is_paredowned = True
                        txn.modified = func.now()
                    txn.update_codes([rule['code']['code_number']] + gst_hst_code_list, 'gst_hst')
                if not txn.qst_signed_off_by_id:
                    if rule['code']['code_number'] not in qst_code_list:
                        txn.is_paredowned = True
                        txn.modified = func.now()
                    txn.update_codes([rule['code']['code_number']] + qst_code_list, 'qst')
                if not txn.pst_signed_off_by_id:
                    if rule['code']['code_number'] not in pst_code_list:
                        txn.is_paredowned = True
                        txn.modified = func.now()
                    txn.update_codes([rule['code']['code_number']] + pst_code_list, 'pst')
                if not txn.apo_signed_off_by_id:
                    if rule['code']['code_number'] not in apo_code_list:
                        txn.is_paredowned = True
                        txn.modified = func.now()
                    txn.update_codes([rule['code']['code_number']] + apo_code_list, 'apo')
                db.session.flush()

    db.session.commit()

    response['message'] = 'Applied paredown for Transactions in Project with id {}'.format(id)
    response['payload'] = []
    create_log(current_user, 'modify', 'User pared down Project', 'ID: ' + str(id))

    return jsonify(response), 200

#===============================================================================
# APPLY PREDICTION MODEL TO A PROJECT
@projects.route('/<int:id>/apply_prediction/', methods=['PUT'])
@jwt_required
@exception_wrapper
#@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def apply_prediction(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()

    request_types = {
        'use_client_model': ['bool'],
    }
    validate_request_data(data, request_types)

    # Get the data to predict
    project = Project.find_by_id(id)
    if not project:
        raise NotFoundError('Project with ID {} does not exist.'.format(id))
    project_transactions = Transaction.query.filter_by(project_id = id).filter(Transaction.approved_user_id is None)
    if project_transactions.count() == 0:
        raise NotFoundError('Project has no transactions to predict.')

    print("Create model.")
    # Get the appropriate active model, create the model object and alter transcation flags
    if data['use_client_model']:
        active_model = ClientModel.find_active_for_client(project.client_id)
        if not active_model:
            raise NotFoundError('No client model has been trained or is active for client ID {}.'.format(project.client_id))
        lh_model = cm.ClientPredictionModel(active_model.pickle)
        project_transactions.update({Transaction.master_model_id: None})
        project_transactions.update({Transaction.client_model_id: active_model.id})
    else:
        active_model = MasterModel.find_active()
        if not active_model:
            raise NotFoundError('No master model has been trained or is active.')
        lh_model = mm.MasterPredictionModel(active_model.pickle)
        project_transactions.update({Transaction.client_model_id: None})
        project_transactions.update({Transaction.master_model_id: active_model.id})

    predictors = active_model.hyper_p['predictors']

    # TODO: fix separation of data so that prediction happens on transactions with IDs
    # Can't assume that final zip lines up arrays properly
    print("Pull transactions to df.")
    df_predict = transactions_to_dataframe(project_transactions)
    print("Preprocessing...")
    df_predict = preprocess_data(df_predict, preprocess_for='prediction', predictors=predictors)

    # Get probability of each transaction being class '1'
    probability_recoverable = [x[1] for x in lh_model.predict_probabilities(df_predict, predictors)]

    project_transactions.update({Transaction.is_predicted: True})
    for tr, pr in zip(project_transactions, probability_recoverable):
        tr.recovery_probability = pr
        tr.modified = func.now()

    db.session.commit()
    response['message'] = 'Prediction successful. Transactions have been marked.'
    create_log(current_user, 'modify', 'User applied prediction to Project', 'ID: ' + str(id))

    return jsonify(response), 201

#===============================================================================
# UPDATE A PROJECT
@projects.route('/<int:id>', methods=['PUT'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def update_project(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
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
    if len(data['name']) < 1 or len(data['name']) > 128:
        raise InputError('Name must be greater than 1 character and no more than 128')

    # scope key checking
    def scopecheck(typecheck, basedata, keys):
        for key in keys:
            if key not in basedata:
                raise InputError('Scope with key {} has not been supplied.'.format(key))
            if typecheck and not isinstance(basedata[key], bool):
                raise InputError('Scope with key {} has wrong data type.'.format(key))
    scopecheck(False, data, ['tax_scope', 'engagement_scope'])
    scopecheck(True, data['tax_scope'], ['has_ts_gst_hst', 'has_ts_qst', 'has_ts_pst', 'has_ts_vat', 'has_ts_mft', 'has_ts_ct', 'has_ts_excise', 'has_ts_customs', 'has_ts_crown', 'has_ts_freehold'])
    scopecheck(False, data['engagement_scope'], ['indirect_tax', 'accounts_payable', 'customs', 'royalties', 'data'])
    scopecheck(True, data['engagement_scope']['indirect_tax'], ['has_es_caps', 'has_es_taxreturn', 'has_es_flowthrough', 'has_es_employeeexpense', 'has_es_pccards', 'has_es_coupons', 'has_es_creditnotes', 'has_es_edi', 'has_es_cars'])
    scopecheck(True, data['engagement_scope']['accounts_payable'], ['has_es_duplpay', 'has_es_unapplcredit', 'has_es_missedearly', 'has_es_otheroverpay'])
    scopecheck(True, data['engagement_scope']['customs'], ['has_es_firmanalysis', 'has_es_brokeranalysis'])
    scopecheck(True, data['engagement_scope']['royalties'], ['has_es_crowngca', 'has_es_crownalloc', 'has_es_crownincent', 'has_es_lornri', 'has_es_lorsliding', 'has_es_lordeduct', 'has_es_lorunder', 'has_es_lormissed'])
    scopecheck(True, data['engagement_scope']['data'], ['has_es_gstreg', 'has_es_cvm', 'has_es_taxgl', 'has_es_aps', 'has_es_ars', 'has_es_fxrates', 'has_es_trt', 'has_es_daf'])

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

    query.has_ts_gst_hst = data['tax_scope']['has_ts_gst_hst']
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
    create_log(current_user, 'modify', 'User updated Project', 'ID: ' + str(id))

    return jsonify(response)

#===============================================================================
# DELETE A PROJECT
@projects.route('/<int:id>', methods=['DELETE'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def delete_project(id):
    response = {'status': 'ok', 'message': '', 'payload': []}

    query = Project.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('Project ID {} does not exist.'.format(id))

    deletedproject = query.serialize
    db.session.delete(query)

    db.session.commit()
    response['message'] = 'Deleted project id {}'.format(deletedproject['id'])
    response['payload'] = [deletedproject]
    create_log(current_user, 'delete', 'User deleted Project', 'ID: ' + str(id))

    return jsonify(response)
