

def j1(caps_gen_id):
    j1 = """
    DROP TABLE IF EXISTS BKPF_VARAP_MSTR;
    select
    L.*,
    ltrim(rtrim(cast(L.data ->> 'bkpf_bukrs_key' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'bkpf_belnr_key' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'bkpf_gjahr_key' AS Text))) varapkey
    into BKPF_VARAP_MSTR
    from
    (select * from sap_bkpf where caps_gen_id = {caps_gen_id}) as L
    """.format(caps_gen_id = caps_gen_id)
    return j1

    #Filtering for fiscal year and working period Nexen ONLY
    #cast(data ->> 'bkpf_gjahr_key' as text) = '2013' and cast(data ->> 'fiscal_period_gl' as text) = '03' and

def j2(caps_gen_id):
    j2 = """
    DROP TABLE IF EXISTS BSEG_AP;
    select
    L.*,
    ltrim(rtrim(cast(L.data ->> 'co_code_gl' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'gl_doc_num' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'fiscal_year_gl' AS Text))) varAPKey,
    cast('' as text) AS varMultiVND,
    cast('' as text) as varSupplier_No
    into  BSEG_AP
    from (select * from sap_bseg where caps_gen_id = {caps_gen_id}) as L
    """.format(caps_gen_id = caps_gen_id)
    return j2

    #Filtering for fiscal year and working period NEXEN ONLY

def j3(caps_gen_id):
    j3 = """
    DROP TABLE IF EXISTS distinctVarAPKeyVendorAcctNum;
    SELECT DISTINCT L.varAPKey, LTRIM(RTRIM(L.data ->> 'vend_num')) AS vend_num, Row_Number() Over(Partition by varAPKey ORDER BY L.data ->> 'vend_num') AS RowNum
    INTO table distinctVarAPKeyVendorAcctNum
    FROM BSEG_AP AS L
    WHERE L.data ->> 'vend_num' IS NOT NULL
                   AND LTRIM(RTRIM(L.data ->> 'vend_num')) != ''
    """
    return j3

def j4(caps_gen_id):
    j4 = """
    DROP TABLE IF EXISTS distinctVarAPKeyMultiVendor;
    SELECT varAPKey, COUNT(*) AS Cnt
    INTO table distinctVarAPKeyMultiVendor
    FROM distinctVarAPKeyVendorAcctNum AS L
    GROUP BY varAPKey
    HAVING COUNT(*) >  1
    """
    return j4

def j5(caps_gen_id):
    j5 = """
    DROP TABLE IF EXISTS bseg_ap_final;
    select
    L.id,
    L.data,
    L.caps_gen_id,
    L.varapkey,
    R1.vend_num,
    R2.varMultiVND
    into table bseg_ap_final
    from bseg_ap as L
    left join (select * from distinctvarAPKeyVendorAcctNum where rownum = 1) as R1
    on L.varapkey = R1.varapkey
    left join (select cast('Multi_Vendor' as TEXT) as varMultiVND, varapkey from distinctvarAPkeymultivendor) as R2
    on L.varapkey = R2.varapkey
    """
    return j5

def j6(caps_gen_id):
    j6 = """
    DROP TABLE IF EXISTS J1_BSEG_BKPF;
    SELECT
    L.varapkey,
	LTRIM(RTRIM(L.data ->> 'main_asset_num')) AS main_asset_num,
	LTRIM(RTRIM(L.data ->> 'asset_sub_num')) AS asset_sub_num,
	LTRIM(RTRIM(L.data ->> 'gl_doc_num')) AS gl_doc_num,
	LTRIM(RTRIM(L.data ->> 'post_key_gl')) AS post_key_gl,
	LTRIM(RTRIM(L.data ->> 'gl_doc_status')) AS gl_doc_status,
	LTRIM(RTRIM(L.data ->> 'bseg_budat_key')) AS bseg_budat_key,
	LTRIM(RTRIM(L.data ->> 'co_code_gl')) AS co_code_gl,
	LTRIM(RTRIM(L.data ->> 'bseg_buzei_key')) AS bseg_buzei_key,
	LTRIM(RTRIM(L.data ->> 'amount_local_ccy')) AS amount_local_ccy,
	LTRIM(RTRIM(L.data ->> 'po_doc_num')) AS po_doc_num,
	LTRIM(RTRIM(L.data ->> 'bseg_ebelp_key')) AS bseg_ebelp_key,
	LTRIM(RTRIM(L.data ->> 'func_area_gl')) AS func_area_gl,
	LTRIM(RTRIM(L.data ->> 'fiscal_year_gl')) AS fiscal_year_gl,
	LTRIM(RTRIM(L.data ->> 'bus_area_dept_num_gl')) AS bus_area_dept_num_gl,
	LTRIM(RTRIM(L.data ->> 'largest_debit_half_acct_num_gl')) AS largest_debit_half_acct_num_gl,
	LTRIM(RTRIM(L.data ->> 'control_area_gl')) AS control_area_gl,
	LTRIM(RTRIM(L.data ->> 'cost_ctr_num_gl')) AS cost_ctr_num_gl,
	LTRIM(RTRIM(L.data ->> 'cx_num')) AS cx_num,
	LTRIM(RTRIM(L.data ->> 'vend_num')) AS vend_num,
	LTRIM(RTRIM(L.data ->> 'material_num_gl')) AS material_num_gl,
	LTRIM(RTRIM(L.data ->> 'tax_type_gl')) AS tax_type_gl,
	LTRIM(RTRIM(L.data ->> 'bseg_mwsk3_key')) AS bseg_mwsk3_key,
	LTRIM(RTRIM(L.data ->> 'po_tax_code_gl')) AS po_tax_code_gl,
	LTRIM(RTRIM(L.data ->> 'gst_hst_qst_pst_local_ccy')) AS gst_hst_qst_pst_local_ccy,
	LTRIM(RTRIM(L.data ->> 'bseg_pargb_key')) AS bseg_pargb_key,
	LTRIM(RTRIM(L.data ->> 'profit_ctr_num')) AS profit_ctr_num,
	LTRIM(RTRIM(L.data ->> 'wbs_gl')) AS wbs_gl,
	LTRIM(RTRIM(L.data ->> 'item_descr_gl')) AS item_descr_gl,
	LTRIM(RTRIM(L.data ->> 'reverse_doc_num')) AS reverse_doc_num,
	LTRIM(RTRIM(L.data ->> 'reverse_reason_gl')) AS reverse_reason_gl,
	LTRIM(RTRIM(L.data ->> 'tax_jur_gl')) AS tax_jur_gl,
	LTRIM(RTRIM(L.data ->> 'sales_doc_num_gl')) AS sales_doc_num_gl,
	LTRIM(RTRIM(L.data ->> 'billing_doc_num')) AS billing_doc_num,
	LTRIM(RTRIM(L.data ->> 'gst_hst_pst_qst_doc_ccy')) AS gst_hst_pst_qst_doc_ccy,
	LTRIM(RTRIM(L.data ->> 'ap_ar_amt_doc_ccy')) AS ap_ar_amt_doc_ccy,
    LTRIM(RTRIM(R.data ->> 'doc_type_gl')) AS doc_type_gl,
    LTRIM(RTRIM(R.data ->> 'inv_date')) AS inv_date,
    LTRIM(RTRIM(R.data ->> 'inv_num')) AS inv_num,
    LTRIM(RTRIM(R.data ->> 'ccy')) AS ccy,
    LTRIM(RTRIM(R.data ->> 'fiscal_period_gl')) AS fiscal_period_gl,
    LTRIM(RTRIM(R.data ->> 'CPUTM')) AS CPUTM,
    LTRIM(RTRIM(R.data ->> 'fx_rate')) AS fx_rate,
    LTRIM(RTRIM(R.data ->> 'trnx_code_gl')) AS trnx_code_gl,
    LTRIM(RTRIM(R.data ->> 'KTOPL')) AS KTOPL,
    LTRIM(RTRIM(R.data ->> 'bkpf_belnr_key')) AS bkpf_belnr_key,
    LTRIM(RTRIM(R.data ->> 'bkpf_bukrs_key')) AS bkpf_bukrs_key,
    LTRIM(RTRIM(R.data ->> 'bkpf_gjahr_key')) AS bkpf_gjahr_key,
    LTRIM(RTRIM(R.data ->> 'bkpf_kzwrs_key')) AS bkpf_kzwrs_key
    into table J1_BSEG_BKPF
    FROM BSEG_AP_final AS L
    INNER JOIN BKPF_VARAP_MSTR AS R
    ON L.varAPKey = R.varAPKey
    """
    return j6

def j7(caps_gen_id):
    j7 = """
    DROP TABLE IF EXISTS J2_BSEG_BKPF_LFA1;
    SELECT L.*,
    LTRIM(RTRIM(R.data ->> 'lfa1_land1_key')) AS lfa1_land1_key,
    LTRIM(RTRIM(R.data ->> 'lfa1_lifnr_key')) AS lfa1_lifnr_key,
    LTRIM(RTRIM(R.data ->> 'vend_name')) AS vend_name,
    LTRIM(RTRIM(R.data ->> 'vend_city')) AS vend_city,
    LTRIM(RTRIM(R.data ->> 'vend_region')) AS vend_region,
    LTRIM(RTRIM(R.data ->> 'vend_tax_num_1')) AS vend_tax_num_1,
    LTRIM(RTRIM(R.data ->> 'vend_tax_num_2')) AS vend_tax_num_2,
    LTRIM(RTRIM(R.data ->> 'vend_tax_num_3')) AS vend_tax_num_3,
    LTRIM(RTRIM(R.data ->> 'vend_tax_num_4')) AS vend_tax_num_4,
    LTRIM(RTRIM(R.data ->> 'vend_tax_num_5')) AS vend_tax_num_5,
    LTRIM(RTRIM(R.data ->> 'vend_tax_num_type')) AS vend_tax_num_type,
    LTRIM(RTRIM(R.data ->> 'vend_reg_num')) AS vend_reg_num
    INTO J2_BSEG_BKPF_LFA1
    FROM J1_BSEG_BKPF AS L
    LEFT JOIN (SELECT * FROM sap_lfa1 WHERE CAST(data ->> 'SPRAS' AS TEXT) = 'EN' and caps_gen_id = {caps_gen_id}) AS R
    ON LTRIM(RTRIM(L.vend_num)) = LTRIM(RTRIM(R.data ->> 'lfa1_lifnr_key'))
    """.format(caps_gen_id = caps_gen_id)
    return j7

def j8(caps_gen_id):
    j8 = """
    DROP TABLE IF EXISTS distinctVarAPKey;

    SELECT CONCAT(L.data ->> 'co_code_gl', '_', L.data ->> 'gl_doc_num', '_', L.data ->> 'fiscal_year_gl') AS varAPKey
    INTO distinctVarAPKey
    FROM sap_bseg AS L
    WHERE cast(L.data ->> 'KOART' as text) = 'K' and caps_gen_id = {caps_gen_id}
    GROUP BY L.data ->> 'co_code_gl', L.data ->> 'gl_doc_num', L.data ->> 'fiscal_year_gl'
    """.format(caps_gen_id = caps_gen_id)
    return j8

def j9(caps_gen_id):
    j9 = """
    DROP TABLE IF EXISTS J3_BSEG_BKPF_LFA1_OnlyAP;

    SELECT L.*
    INTO J3_BSEG_BKPF_LFA1_OnlyAP
    FROM J2_BSEG_BKPF_LFA1 AS L
    INNER JOIN distinctVarAPKey AS R
    ON L.varAPKey = R.varAPKey
    """
    return j9

def j10(caps_gen_id):
    j10 = """
    DROP TABLE IF EXISTS j4_BSEG_BKPF_LFA1_T001_OnlyAP;
    select L.*,
    R.data ->> 't001_bukrs_key' as t001_bukrs_key,
    R.data ->> 'co_name' as co_name,
    R.data ->> 'KTOPL'  as t001_ktopl_key
    into j4_BSEG_BKPF_LFA1_T001_OnlyAP
    from (select * from j3_BSEG_BKPF_LFA1_OnlyAP) as L
    inner join (select * from sap_t001 where caps_gen_id = {caps_gen_id}) as R
    on L.co_code_gl = R.data ->> 't001_bukrs_key'
    """.format(caps_gen_id = caps_gen_id)
    return j10

    #fiscal_year_gl =  '2013' NEXEN ONLY

def j10point5(caps_gen_id):
    j10point5 = """
    DELETE FROM sap_aps WHERE caps_gen_id = {caps_gen_id};
    INSERT INTO sap_aps (caps_gen_id, main_asset_num,
    asset_sub_num,
    gl_doc_num,
    post_key_gl,
    gl_doc_status,
    bseg_budat_key,
    co_code_gl,
    bseg_buzei_key,
    amount_local_ccy,
    po_doc_num,
    bseg_ebelp_key,
    func_area_gl,
    fiscal_year_gl,
    bus_area_dept_num_gl,
    largest_debit_half_acct_num_gl,
    control_area_gl,
    cx_num,
    vend_num,
    material_num_gl,
    tax_type_gl,
    bseg_mwsk3_key,
    po_tax_code_gl,
    gst_hst_qst_pst_local_ccy,
    bseg_pargb_key,
    profit_ctr_num,
    wbs_gl,
    item_descr_gl,
    reverse_doc_num,
    reverse_reason_gl,
    tax_jur_gl,
    sales_doc_num_gl,
    billing_doc_num,
    gst_hst_pst_qst_doc_ccy,
    ap_ar_amt_doc_ccy,
    doc_type_gl,
    inv_date,
    inv_num,
    ccy,
    fiscal_period_gl,
    fx_rate,
    trnx_code_gl,
    bkpf_belnr_key,
    bkpf_bukrs_key,
    bkpf_gjahr_key,
    bkpf_kzwrs_key,
    lfa1_land1_key,
    lfa1_lifnr_key,
    vend_name,
    vend_city,
    vend_region,
    vend_tax_num_1,
    vend_tax_num_2,
    vend_tax_num_3,
    vend_tax_num_4,
    vend_tax_num_5,
    vend_tax_num_type,
    vend_reg_num,
    cost_ctr_num_gl,
    skat_ktopl_key,
    skat_saknr_key,
    skat_spras_key,
    lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl)
    select
    {caps_gen_id} caps_gen_id,
    L.main_asset_num,
    L.asset_sub_num,
    L.gl_doc_num,
    L.post_key_gl,
    L.gl_doc_status,
    L.bseg_budat_key,
    L.co_code_gl,
    L.bseg_buzei_key,
    L.amount_local_ccy,
    L.po_doc_num,
    L.bseg_ebelp_key,
    L.func_area_gl,
    L.fiscal_year_gl,
    L.bus_area_dept_num_gl,
    L.largest_debit_half_acct_num_gl,
    L.control_area_gl,
    L.cx_num,
    L.vend_num,
    L.material_num_gl,
    L.tax_type_gl,
    L.bseg_mwsk3_key,
    L.po_tax_code_gl,
    L.gst_hst_qst_pst_local_ccy,
    L.bseg_pargb_key,
    L.profit_ctr_num,
    L.wbs_gl,
    L.item_descr_gl,
    L.reverse_doc_num,
    L.reverse_reason_gl,
    L.tax_jur_gl,
    L.sales_doc_num_gl,
    L.billing_doc_num,
    L.gst_hst_pst_qst_doc_ccy,
    L.ap_ar_amt_doc_ccy,
    L.doc_type_gl,
    L.inv_date,
    L.inv_num,
    L.ccy,
    L.fiscal_period_gl,
    L.fx_rate,
    L.trnx_code_gl,
    L.bkpf_belnr_key,
    L.bkpf_bukrs_key,
    L.bkpf_gjahr_key,
    L.bkpf_kzwrs_key,
    L.lfa1_land1_key,
    L.lfa1_lifnr_key,
    L.vend_name,
    L.vend_city,
    L.vend_region,
    L.vend_tax_num_1,
    L.vend_tax_num_2,
    L.vend_tax_num_3,
    L.vend_tax_num_4,
    L.vend_tax_num_5,
    L.vend_tax_num_type,
    L.vend_reg_num,
    L.cost_ctr_num_gl,
    R.data ->>   'skat_ktopl_key' as skat_ktopl_key,
    R.data ->>   'skat_saknr_key' as skat_saknr_key,
    R.data ->>   'skat_spras_key' as skat_spras_key,
    R.data ->>   'lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl' as lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl
    from j4_BSEG_BKPF_LFA1_T001_OnlyAP as L
    inner join (select * from sap_skat where caps_gen_id = {caps_gen_id}) as R
    on L.largest_debit_half_acct_num_gl = R.data ->> 'skat_saknr_key'
    and
    L.T001_KTOPL_KEY = R.data ->> 'skat_ktopl_key'
    """.format(caps_gen_id = caps_gen_id)
    return j10point5
