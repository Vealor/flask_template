#!/bin/bash

# DEVELOPMENT


DB_URL=localhost #1
FLASK_ENV=development #2  development, testing, production
USERNAME=itra #3
DATABASE=itra_db #4
PASSWORD=LHDEV1234 #5
PORT=5000 #6
BACKEND=http://localhost #7
# TESTING
if [[ $1 == *"test"* ]]; then
  echo "TESTING"
  DB_URL=itra-uat-sql.postgres.database.azure.com #1
  FLASK_ENV=testing #2
  USERNAME=lh_admin_tax@itra-uat-sql.postgres.database.azure.com #3
  DATABASE=itra_db #4
  PASSWORD=Kpmg1234@ #5
  PORT=443 #6
  BACKEND=https://itra-backend-uat.azurewebsites.net #7

# PRODUCTION
elif [[ $1 == *"prod"* ]]; then
  echo "PRODUCTION"
  DB_URL=localhost #1
  FLASK_ENV=production #2
  USERNAME=itra #3
  DATABASE=itra_db #4
  PASSWORD=LHDEV1234 #5
  PORT=5000 #6
  BACKEND=http://localhost #7
fi


# sed -i 's/|4$/|15/g' ../sap_caps_all_fiscal_years.csv
# PGPASSWORD=$PASSWORD psql -h $DB_URL -U $USERNAME $DATABASE -c "\\copy sap_aps(
# id,bkpf_belnr_key,doc_type_gl,inv_date,post_date_gl,bkpf_bukrs_key,bkpf_gjahr_key,fx_rate,bkpf_kzwrs_key,fiscal_period_gl,trnx_code_gl,ccy,inv_num,main_asset_num,asset_sub_num,gl_doc_num,post_key_gl,gl_doc_status,bseg_budat_key,co_code_gl,bseg_buzei_key,amount_local_ccy,po_doc_num,bseg_ebelp_key,func_area_gl,fiscal_year_gl,bus_area_dept_num_gl,largest_debit_half_acct_num_gl,control_area_gl,cost_ctr_num_gl,cx_num,vend_num,material_num_gl,tax_type_gl,bseg_mwsk3_key,po_tax_code_gl,gst_hst_qst_pst_local_ccy,bseg_pargb_key,profit_ctr_num,wbs_gl,item_descr_gl,reverse_doc_num,reverse_reason_gl,tax_jur_gl,sales_doc_num_gl,billing_doc_num,gst_hst_pst_qst_doc_ccy,ap_ar_amt_doc_ccy,lfa1_land1_key,lfa1_lifnr_key,vend_name,vend_city,vend_region,vend_tax_num_1,vend_tax_num_2,vend_tax_num_3,vend_tax_num_4,vend_tax_num_5,vend_tax_num_type,vend_reg_num,skat_ktopl_key,skat_saknr_key,skat_spras_key,lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl,caps_gen_id,bkpf_ktopl_key,bseg_dmbe2_key,bseg_pswbt_key,bseg_shkzg_key,bseg_umskz_key,varapkey
# ) from '../sap_aps.csv' HEADER DELIMITER '|' CSV QUOTE '\"' ESCAPE '''';"

# sed -i 's/|$old_id|/|$new_id|/g' ./../caps_50_final.csv
PGPASSWORD=$PASSWORD psql -h $DB_URL -U $USERNAME $DATABASE -c "\\copy sap_caps(
transaction_attributes,
    even_gst_ind,
    odd_imm,
    prov_ap_amt,
    pme_imm,
    gst_imm,
    gst_count,
    cn_flag_ind,
    cn_rep2_ind,
    prov_ap,
    even_gst_rate,
    even_hst13_rate,
    even_hst14_rate,
    even_hst15_rate,
    even_gst_bc_rate,
    even_gst_mb_rate,
    even_gst_sask_rate,
    even_gst_qst_rate,
    pme_mat,
    gst_mat,
    flag_cn,
    odd_ind,
    pme_general,
    prov_tax_ind,
    eff_rate,
    rate_ind,
    new_vend_name,
    net_value,
    top_inv_amt,
    amount_local_ccy,
    ap_ar_amt_doc_ccy,
    vardocamt,
    vartranamount,
    varlocamt,
    ap_amt,
    gst_hst,
    pst,
    pst_sa,
    qst,
    taxes_other,
    varapkey,
    doc_type_gl,
    inv_date,
    post_date_gl,
    fx_rate,
    fiscal_period_gl,
    trnx_code_gl,
    ccy,
    inv_num,
    main_asset_num,
    asset_sub_num,
    gl_doc_num,
    post_key_gl,
    gl_doc_status,
    co_code_gl,
    po_doc_num,
    func_area_gl,
    fiscal_year_gl,
    bus_area_dept_num_gl,
    control_area_gl,
    cost_ctr_num_gl,
    cx_num,
    vend_num,
    material_num_gl,
    tax_type_gl,
    po_tax_code_gl,
    gst_hst_qst_pst_local_ccy,
    profit_ctr_num,
    profit_ctr_name,
    profit_ctr_descr,
    cost_ctr_name,
    cost_ctr_descr,
    wbs_gl,
    item_descr_gl,
    reverse_doc_num,
    reverse_reason_gl,
    tax_jur_gl,
    sales_doc_num_gl,
    billing_doc_num,
    gst_hst_pst_qst_doc_ccy,
    vend_name,
    vend_city,
    vend_region,
    vend_cntry,
    vend_tax_num_1,
    vend_tax_num_2,
    vend_tax_num_3,
    vend_tax_num_4,
    vend_tax_num_5,
    vend_tax_num_type,
    vend_reg_num,
    lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl,
    post_key_descr,
    co_name,
    proj_loc_proj,
    proj_type_proj,
    wbs_elem_descr_proj,
    wbs_elem_id_proj,
    wbs_cntrl_area_proj,
    wbs_bus_area_proj,
    jv_obj_type_proj,
    object_num_proj,
    proj_descr_proj,
    proj_defin_proj,
    proj_internal_proj,
    proj_tx_jur_proj,
    proj_mngr_name_proj,
    proj_mngr_num_proj,
    bus_area_proj,
    plant_proj,
    tx_jur_descr_tx,
    plant_name_plant,
    plant_tx_jur_plant,
    tx_name_tx,
    largest_debit_half_acct_num_gl,
    pymt_doc_num_pmt,
    payee_code_pmt,
    cx_num_pmt,
    co_code_pmt,
    incoterms1,
    incoterms2,
    cntry_name,
    ean_upc_num_mat,
    mat_orig_ctry_mat,
    ean_categ_mat,
    mat_tx_class_mat,
    mat_tx_class_descr_mat,
    mat_group_descr_mat,
    mat_descr_mat,
    mat_dept_ctry_mat,
    mat_tx_ind_mat,
    wbs_po,
    po_tx_code_po,
    plant_num,
    po_tx_jur,
    po_item_descr,
    stor_loc_desc_mat,
    stor_loc_mat,
    stor_plant_mat,
    mat_doc_num_mat,
    mat_plnt_mat,
    punch_grp_po,
    punch_org_po,
    handover_loc_po,
    vend_phone,
    vend_person,
    purch_org_descr_po,
    caps_gen_id
) from '../sap_caps_all_fiscal_years.csv' HEADER DELIMITER '|' CSV QUOTE '\"' ESCAPE '''';"
