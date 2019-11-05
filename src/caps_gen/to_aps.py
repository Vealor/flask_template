

def j1(caps_gen_id):
    j1 = """
    DROP TABLE IF EXISTS BKPF_VARAP_MSTR;
    select
    L.*,
    ltrim(rtrim(cast(L.data ->> 'bkpf_bukrs_key' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'bkpf_belnr_key' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'bkpf_gjahr_key' AS Text))) varapkey
    into BKPF_VARAP_MSTR
    from
    (select * from sap_bkpf where cast(data ->> 'bkpf_gjahr_key' as text) = '2013' and cast(data ->> 'fiscal_period_gl' as text) = '03' and caps_gen_id = {caps_gen_id}) as L
    """.format(caps_gen_id = caps_gen_id)
    return j1

def j2(caps_gen_id):
    j2 = """
    DROP TABLE IF EXISTS BSEG_AP;
    select
    L.*,
    ltrim(rtrim(cast(L.data ->> 'co_code_gl' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'gl_doc_num' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'fiscal_year_gl' AS Text))) varAPKey,
    cast('' as text) AS varMultiVND,
    cast('' as text) as varSupplier_No
    into  BSEG_AP
    from (select * from sap_bseg where cast(data ->> 'fiscal_year_gl' as text) = '2013' and capsgen_id = {capsgen_id}) as L
    """.format(caps_gen_id = caps_gen_id)
    return j2

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
    L.capsgen_id,
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
    SELECT L.*,
    LTRIM(RTRIM(R.data ->> 'doc_type_gl')) AS doc_type_gl,
    LTRIM(RTRIM(R.data ->> 'inv_date')) AS inv_date,
    LTRIM(RTRIM(R.data ->> 'inv_num')) AS inv_num,
    LTRIM(RTRIM(R.data ->> 'ccy')) AS ccy,
    LTRIM(RTRIM(R.data ->> 'fiscal_period_gl')) AS fiscal_period_gl,
    LTRIM(RTRIM(R.data ->> 'CPUTM')) AS CPUTM,
    LTRIM(RTRIM(R.data ->> 'fx_rate')) AS fx_rate,
    LTRIM(RTRIM(R.data ->> 'trnx_code_gl')) AS trnx_code_gl,
    LTRIM(RTRIM(R.data ->> 'KTOPL')) AS KTOPL
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
    LTRIM(RTRIM(R.data ->> 'vend_name')) AS vend_name,
    LTRIM(RTRIM(R.data ->> 'NAME2')) AS NAME2,
   LTRIM(RTRIM(R.data ->> 'lfa1_land1_key')) AS lfa1_land1_key,
   LTRIM(RTRIM(R.data ->> 'vend_region')) AS vend_region,
   LTRIM(RTRIM(R.data ->> 'vend_city')) AS vend_city,
   LTRIM(RTRIM(R.data ->> 'PSTLZ')) AS PSTLZ,
   LTRIM(RTRIM(R.data ->> 'STRAS')) AS STRAS
    INTO J2_BSEG_BKPF_LFA1
    FROM J1_BSEG_BKPF AS L
    LEFT JOIN (SELECT * FROM sap_lfa1 WHERE CAST(data ->> 'SPRAS' AS TEXT) = 'EN' and capsgen_id = {capsgen_id}) AS R
    ON LTRIM(RTRIM(L.data ->> 'vend_num')) = LTRIM(RTRIM(R.data ->> 'lfa1_lifnr_key'))
    """.format(caps_gen_id = caps_gen_id)
    return j7

def j8(caps_gen_id):
    j8 = """
    DROP TABLE IF EXISTS distinctVarAPKey;

    SELECT CONCAT(L.data ->> 'co_code_gl', '_', L.data ->> 'gl_doc_num', '_', L.data ->> 'fiscal_year_gl') AS varAPKey
    INTO distinctVarAPKey
    FROM sap_bseg AS L
    WHERE cast(L.data ->> 'KOART' as text) = 'K' and capsgen_id = {capsgen_id}
    GROUP BY L.data ->> 'co_code_gl', L.data ->> 'gl_doc_num', L.data ->> 'fiscal_year_gl'
    """.format(caps_gen_id = caps_gen_id)
    return j8

def j9(caps_gen_id):
    j9 = """
    DROP TABLE IF EXISTS J3_BSEG_BKPF_LFA1_OnlyAP;

    SELECT L.*
    INTO APS
    FROM J2_BSEG_BKPF_LFA1 AS L
    INNER JOIN distinctVarAPKey AS R
    ON L.varAPKey = R.varAPKey
    """
    return j9

def j10(caps_gen_id):
    j10 = """
    select L.*,
    R.data ->> 't001_bukrs_key' as t001_bukrs_key,
    R.data ->> 'co_name' as co_name,
    R.data ->> 'KTOPL'  as t001_ktopl
    from (select * from j3_BSEG_BKPF_LFA1_OnlyAP where cast(data ->> 'fiscal_year_gl' as text) = '2013') as L
    left join (select * from sap_t001 where capsgen_id = {capsgen_id}) as R
    on L.data ->> 'co_code_gl' = R.data ->> 't001_bukrs_key
    """.format(caps_gen_id = caps_gen_id)
    return j10
