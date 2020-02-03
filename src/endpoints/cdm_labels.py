'''
CDMLabel Endpoints
'''
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.models import CDMLabel
from src.wrappers import has_permission, exception_wrapper

cdm_labels = Blueprint('cdm_labels', __name__)
#===============================================================================
# GET ALL DATA MAPPINGS
@cdm_labels.route('/', methods=['GET'])
@jwt_required
@exception_wrapper
@has_permission(['tax_practitioner', 'tax_approver', 'tax_master', 'data_master', 'administrative_assistant'])
def get_cdm_labels():
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = CDMLabel.query
    # Set ORDER
    query = query.order_by('script_label')

    if 'caps_table' in args.keys():
        output = {}
        for i in query.all():
            output[i.script_label] = {'display_name': i.display_name, 'caps_interface': i.caps_interface.value if i.caps_interface else None}
        response['payload'] = output
    else:
        response['payload'] = [i.serialize for i in query.all()]
    response['order'] = [
        'flags',
        'transaction_attributes',
        'recovery_probability',
        'has_recoverable',
        'coding_data',
        'inv_date',
        'inv_num',
        'post_date_gl',
        'post_key_gl',
        'post_key_descr',
        'doc_type_gl',
        'doc_type_descr',
        'vend_num',
        'vend_name',
        'vend_reg_num',
        'vend_tax_num_type',
        'vend_city',
        'vend_region',
        'vend_phone',
        'vend_person',
        'ccy',
        'ccy_descr',
        'amount_local_ccy',
        'gst_hst_qst_pst_local_ccy',
        'ap_ar_amt_doc_ccy',
        'gst_hst_pst_qst_doc_ccy',
        'item_descr_gl',
        'largest_debit_half_acct_num_gl',
        'func_area_gl',
        'assign_num_gl',
        'bus_area_dept_num_gl',
        'bus_area_dept_name_gl',
        'control_area_gl',
        'cost_ctr_num_gl',
        'cost_ctr_name',
        'cost_ctr_descr',
        'cost_ctr_tx_jur',
        'material_num_gl',
        'mat_descr_mat',
        'mat_doc_num_mat',
        'mat_group_descr_mat',
        'mat_plnt_mat',
        'plant_name_plant',
        'plant_tx_jur_plant',
        'mat_orig_ctry_mat',
        'mat_dept_ctry_mat',
        'mat_tx_ind_mat',
        'mat_tx_ind_descr_mat',
        'mat_tx_class_mat',
        'mat_tx_class_descr_mat',
        'ean_upc_num_mat',
        'ean_categ_mat',
        'ean_categ_descr_mat',
        'stor_loc_desc_mat',
        'stor_loc_mat',
        'stor_plant_mat',
        'profit_ctr_num',
        'profit_ctr_name',
        'profit_ctr_descr',
        'profit_ctr_tx_jur',
        'wbs_gl',
        'wbs_po',
        'wbs_bus_area_proj',
        'wbs_cntrl_area_proj',
        'wbs_elem_id_proj',
        'wbs_elem_descr_proj',
        'proj_internal_proj',
        'proj_defin_proj',
        'proj_descr_proj',
        'proj_tx_jur_proj',
        'proj_type_proj',
        'proj_loc_proj',
        'bus_area_proj',
        'plant_proj',
        'object_num_proj',
        'jv_obj_type_proj',
        'incoterms1',
        'incoterms1_descr',
        'incoterms2',
        'po_doc_num',
        'po_item_descr',
        'po_tax_code_gl',
        'tx_name_tx',
        'po_tx_code_po',
        'po_tx_jur',
        'punch_grp_po',
        'purch_group_descr_po',
        'punch_org_po',
        'purch_org_descr_po',
        'plant_num',
        'handover_loc_po',
        'reverse_doc_num',
        'reverse_reason_gl',
        'pymt_dt_pmt',
        'pymt_method_pmt',
        'pymt_doc_num_pmt',
        'check_num_pmt',
        'pymt_period_gl',
        'pymt_terms_gl',
        'co_code_pmt',
        'payee_code_pmt',
        'tax_type_gl',
        'tx_type_descr_tx',
        'tax_jur_gl',
        'tx_jur_descr_tx',
        'cash_disc_percent_1_gl',
        'cash_disc_days_1_gl',
        'cash_disc_percent_2_gl',
        'cash_disc_days_2_gl',
        'fx_rate',
        'co_code_gl',
        'co_name',
        'fiscal_year_gl',
        'fiscal_period_gl',
        'gl_doc_num',
        'gl_doc_status',
        'trnx_code_gl',
        'spec_trnx_type_gl',
        'spec_indicator_gl'
    ]

    return jsonify(response)
