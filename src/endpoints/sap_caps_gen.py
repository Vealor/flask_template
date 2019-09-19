'''
sap_caps_gen endpoints
'''
import csv
import json
import os
import re
import zipfile
import requests
import sqlalchemy
from collections import Counter
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from sqlalchemy.sql import expression, functions
from config import *

sap_caps_gen = Blueprint('sap_caps_gen', __name__)

def get_cwd(read_path):
    current_directory = os.path.dirname(os.path.abspath('__file__'))
    current_file_path = os.path.join(current_directory, read_path)
    return current_file_path

def mapping_serializer(label):
    return {
        "script_label": label.script_labels,
        "mappings": [{"column_name": map.column_name, "table_name" : map.table_name} for map in label.cdm_label_data_mappings.all()]
    }

#helper function to recursively unzip files within a folder
def extract_nested_zip(zippedFile, toFolder):
    try:
        with zipfile.ZipFile(zippedFile, 'r') as zfile:
            zfile.extractall(path=toFolder)
    except NotImplementedError:
        raise Exception(str(zippedFile) + ' has compression errors. Please fix')
    except Exception as e:
        raise Exception('Unable to work with file ' + str(zippedFile))
    os.remove(zippedFile)
    for root, dirs, files in os.walk(toFolder):
        for filename in files:
            if re.search(r'\.(?i)ZIP$', filename):
                fileSpec = os.path.join(root, filename)
                extract_nested_zip(fileSpec, root)
#This takes the source data, in the form of a zip file, located in caps_gen_raw, and unzips it into caps_gen_unzipped.
#The endpoint can go through nested folders/zips.
@sap_caps_gen.route('/unzipping', methods=['POST'])
def unzipping():
    response = {'status': 'ok', 'message': '', 'payload': {'files_skipped': []}}
    data = request.get_json()
    try:
        current_input_path = get_cwd('caps_gen_processing/caps_gen_raw')
        current_output_path = get_cwd('caps_gen_processing/caps_gen_unzipped')
        cwd = os.getcwd()
        os.chdir(current_input_path)
        extension = '.zip'
        for item in os.listdir(current_input_path):
            if item.lower().endswith(extension):
                try:
                    extract_nested_zip(item, current_output_path)
                except Exception as e:
                    response['status'] = 'Cannot unzip input zip'
                    response['message'] = response['message'] + ('Failed on ' + str(item))
            else:
                response['payload']['files_skipped'].append(item.lower())
        os.chdir(cwd)
    except Exception as e:
        return response
        #except Exception as e:
            #response['message'] = 'Successfully downloaded, but unable to access caps_gen_unzipped folder'
            #return 'Unable to access folder.'
    print('Data Received: "{data}"'.format(data=data))
    return response

#MAPPING HAPPENS: The CDM labels + Data Mappings table needs to be populated. See db_refresh.sh
@sap_caps_gen.route('/build_master_tables', methods=['GET'])
def build_master_tables():
    response = {'status': 'ok', 'message': {}, 'payload': {}}
    try:
        mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
        list_tablenames = list(set([table['mappings'][0]['table_name'] for table in mapping]))
        #list_tablenames = ['T007S']

        for table in list_tablenames:
            table_results = {}
            table_files = []

            #Search for all files that match table
            for file in os.listdir(get_cwd('caps_gen_processing/caps_gen_unzipped')):
                if re.search(table, file):
                    if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
                        table_files.append(file)
            print(table_files)

            #Load & union files into one master table in memory
            wfd = open(get_cwd(os.path.join('caps_gen_processing/caps_gen_master', '{}_MASTER.txt'.format(table))), 'wb')
            for index, file in enumerate(table_files):
                if index == 0:
                    with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_unzipped', file)), 'r' ,encoding='utf-8-sig') as fd:
                        #first_line = fd.readline()
                        #table_results['header'] = first_line
                        #first_line = first_line.encode()
                        #wfd.write(first_line)
                        wfd.write(fd.read().encode())
                else:
                    # for all future files
                    with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_unzipped', file)), 'r', encoding='utf-8-sig') as fd:
                        #   strip header
                        next(fd)
                        wfd.write(fd.read().encode())
            wfd.close()

            #initialize variables for bulk insertion
            referenceclass = eval('Sap' + str(table.lower().capitalize()))
            bulk_insert_handler = []

            #bulk insert into database
            with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_master', '{}_MASTER.txt'.format(table))), 'r', encoding='utf-8-sig') as masterfile:
                #masterfile = [next(masterfile) for x in range(10000)]
                for line in csv.DictReader((line.replace('#|#', 'ø') for line in masterfile), delimiter='ø', quoting=csv.QUOTE_NONE):
                    dict_to_insert = {'data' : line}
                    dict_to_insert['project_id'] = 1
                    bulk_insert_handler.append(dict_to_insert)
            db.session.bulk_insert_mappings(referenceclass, bulk_insert_handler)
            db.session.commit()
            print('great success')
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        return response
    return response

######################### MAPPING HAPPENS HERE #######################################

#renames columns as per mapping. Do not run this yet if you plan to execute J1 to J10; as the joins are currently hardcoded to their original names.
#the top priority is to complete caps; and CDM is not final yet so CDM labels will not be written in.
@sap_caps_gen.route('/rename_scheme', methods=['GET'])
def rename_scheme():
    #jsonify DB query
    def rename_query_serializer(row):
        return {
            "id": row.id,
            "data": row.data
        }

    response = {'status': 'ok', 'message': {}, 'payload': {}}
    try:
        mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
        list_tablenames = list(set([table['mappings'][0]['table_name'] for table in mapping]))
        for table in list_tablenames:
            renamed_columndata = []
            rename_scheme = {}
            for index, elem in enumerate(mapping):
                if mapping[index]['mappings'][0]['table_name'] == table:
                    rename_scheme.update({mapping[index]['mappings'][0]['column_name']: mapping[index]['script_label']})
            tableclass = eval('Sap' + str(table.lower().capitalize()))
            columndata = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).all()
            for row in columndata:
                try:
                    row = rename_query_serializer(row)
                    for key, value in renaming_scheme.items():
                        row['data'][value] = row['data'].pop(key)
                except KeyError as e:
                    print('missing CDM label column' + str(e))
                renamed_columndata.append(row)
            db.session.bulk_update_mappings(tableclass, renamed_columndata)
            db.session.commit()
    except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
    return 'OK'
#this performs 3 quality checks - checking for validity (regex), completeness (nulls/total cols), uniqueness (uniqueness of specified key grouping from data dictionary)
@sap_caps_gen.route('/data_quality_check', methods=['GET'])
def data_quality_check():
    def regex_serializer(row):
        return {
            'data' : row.data
        }
    def unique_key_serializer(row, unique_keys):
        return {
            "unique_key" : [row.data[x] for x in unique_keys]
        }

    def data_dictionary(mapping, table):
        rename_dict = {}
        for index, elem in enumerate(mapping):
            if mapping[index]['mappings'][0]['table_name'] == table:
                rename_dict.update({mapping[index]['script_label']: {
                    'is_calculated': mapping[index]['is_calculated'],
                    'is_required': mapping[index]['is_required'],
                    'is_unique': mapping[index]['is_unique'],
                    'regex': mapping[index]['regex'],
                }})
        return rename_dict

    def retrieve_dq_serializer(label):
        return {
            "script_label": label.script_labels,
            "is_required": label.is_required,
            "regex": label.regex,
            "is_unique": label.is_unique,
            "is_calculated": label.is_calculated,
            "mappings": [{"column_name": map.column_name, "table_name": map.table_name} for map in
                         label.cdm_label_data_mappings.all()]
        }

    def validity_check(result, regex):
        validity_response = {}
        results = list(filter(re.compile(regex).match, result))
        validity_response['results'] = results
        validity_response['final_score'] = 100 - (len(validity_response['results'])/len(column))
        return validity_response

    data_dictionary_results = {
    }
    CDM_query = [retrieve_dq_serializer(label) for label in CDM_label.query.all()]
    list_tablenames = list(set([table['mappings'][0]['table_name'] for table in CDM_query if table['mappings']]))
    for table in list_tablenames:
        data_dictionary_results[table] = {}
        tableclass = eval('Sap' + str(table.lower().capitalize()))
        compiled_data_dictionary = data_dictionary(CDM_query, table)

        ### UNIQUENESS CHECK ###
        #The argument should be set to true when some of is_unique column in CDM labels is set to True.
        unique_keys = [x for x in compiled_data_dictionary if compiled_data_dictionary[x]['is_unique'] == False]
        if unique_keys:
            print(unique_keys)
            unique_key_checker = []
            data = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).all()
            for row in data:
                row = unique_key_serializer(row, unique_keys)
                ''.join(row)
                unique_key_checker.append(row['unique_key'])
            c = Counter(map(tuple, unique_key_checker))
            dups = [k for k, v in c.items() if v > 1]
        #if there are no unique keys, line below will bug out, saying its not being referenced. This is because dups above never runs so the var does not initialize.
        if len(dups) > 1:
            uniqueness_response = {}
            uniqueness_response['results'] = dups
            uniqueness_response['final_score'] = 100 - (len(dups)/tableclass.query.count())
            data_dictionary_results[table] = {'uniqueness' : uniqueness_response}
        ### completeness check ###
        for column in compiled_data_dictionary.keys():
            completeness_response = {}
            print(column)
            column = 'company_code'
            query = tableclass.query
            query = query.with_entities(getattr(tableclass, 'data')).all()
            query = [regex_serializer(row)['data'][column] for row in query]
        ### validity check ###
            if compiled_data_dictionary[column]['regex']:
                data_dictionary_results[table][column] = {
                    'regex': validity_check(query, compiled_data_dictionary[column]['regex'])}
    return data_dictionary_results

import datetime

#j1 to j10 joins to create APS
@sap_caps_gen.route('/j1_j10', methods=['GET'])
def j1_j10():
    def execute(query):
        print(str(datetime.datetime.now()))
        print("Executing...")
        result = db.session.execute(query)
        print("Committing...")
        db.session.commit()
        print("Done.")
        return 'query execute successful'

    response = {'status': 'ok', 'message': {}, 'payload': {}}

    j1 = """DROP TABLE IF EXISTS JOIN_BKPF_T001_MSTR;
    select
    L.*,
    R.data ->> 'KTOPL' as KTOPL,
    ltrim(rtrim(cast(L.data ->> 'BUKRS' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'BELNR' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'GJAHR' AS Text))) varapkey
    into table JOIN_BKPF_T001_MSTR
    from
    (select * from sap_bkpf) as L
    inner join
    (select * from sap_t001 where CAST(data ->> 'SPRAS' AS TEXT) = 'EN') as R
    on CAST(L.data -> 'BUKRS' AS TEXT) = cast(R.data -> 'BUKRS' AS TEXT)
    """


    j2 = """DROP TABLE IF EXISTS BSEG_AP;
    select
    L.*,
    ltrim(rtrim(cast(L.data ->> 'BUKRS' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'BELNR' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'GJAHR' AS Text))) varAPKey,
    cast('' as text) AS varMultiVND,
    cast('' as text) as varSupplier_No
    into  BSEG_AP
    from (select * from sap_bseg) as L"""

    # Set the
    j3 = """
    DROP TABLE IF EXISTS distinctVarAPKeyVendorAcctNum;
    SELECT DISTINCT L.varAPKey, LTRIM(RTRIM(L.data ->> 'LIFNR')) AS LIFNR, Row_Number() Over(Partition by varAPKey ORDER BY L.data ->> 'LIFNR') AS RowNum
    INTO table distinctVarAPKeyVendorAcctNum
    FROM BSEG_AP AS L
    WHERE L.data ->> 'LIFNR' IS NOT NULL
                   AND LTRIM(RTRIM(L.data ->> 'LIFNR')) != ''
    """

    j4 = """
    DROP TABLE IF EXISTS distinctVarAPKeyMultiVendor;
    SELECT varAPKey, COUNT(*) AS Cnt
    INTO table distinctVarAPKeyMultiVendor
    FROM distinctVarAPKeyVendorAcctNum AS L
    GROUP BY varAPKey
    HAVING COUNT(*) >  1
    """

#Update Vendor Account Number for each varAPKey if Vendor Account Number is null with the first vendor account number

    j5 = """
        DROP TABLE IF EXISTS bseg_ap_final;
    select
    L.id,
    L.data,
    L.project_id,
    L.varapkey,
    R1.LIFNR,
    R2.varMultiVND
    into table bseg_ap_final
    from bseg_ap as L
    left join (select * from distinctvarAPKeyVendorAcctNum where rownum = 1) as R1
    on L.varapkey = R1.varapkey
    left join (select cast('Multi_Vendor' as TEXT) as varMultiVND, varapkey from distinctvarAPkeymultivendor) as R2
    on L.varapkey = R2.varapkey
    """



    j6 = """
    DROP TABLE IF EXISTS J1_BSEG_BKPF;
    SELECT L.*,
    LTRIM(RTRIM(R.data ->> 'BLART')) AS BLART,
    LTRIM(RTRIM(R.data ->> 'BLDAT')) AS BLDAT,
    LTRIM(RTRIM(R.data ->> 'XBLNR')) AS XBLNR,
    LTRIM(RTRIM(R.data ->> 'WAERS')) AS WAERS,
    LTRIM(RTRIM(R.data ->> 'MONAT')) AS MONAT,
    LTRIM(RTRIM(R.data ->> 'CPUTM')) AS CPUTM,
    LTRIM(RTRIM(R.data ->> 'KURSF')) AS KURSF,
    LTRIM(RTRIM(R.data ->> 'TCODE')) AS TCODE,
    LTRIM(RTRIM(R.data ->> 'KTOPL')) AS KTOPL
    into table J1_BSEG_BKPF
    FROM BSEG_AP_final AS L
    INNER JOIN JOIN_BKPF_T001_MSTR AS R
    ON L.varAPKey = R.varAPKey
    """

    j7 = """
    DROP TABLE IF EXISTS J2_BSEG_BKPF_LFA1;
    SELECT L.*, LTRIM(RTRIM(R.data ->> 'NAME1')) AS NAME1, LTRIM(RTRIM(R.data ->> 'NAME2')) AS NAME2,
               LTRIM(RTRIM(R.data ->> 'LAND1')) AS LAND1, LTRIM(RTRIM(R.data ->> 'REGIO')) AS REGIO, LTRIM(RTRIM(R.data ->> 'ORT01')) AS ORT01,
               LTRIM(RTRIM(R.data ->> 'PSTLZ')) AS PSTLZ, LTRIM(RTRIM(R.data ->> 'STRAS')) AS STRAS
    INTO J2_BSEG_BKPF_LFA1
    FROM J1_BSEG_BKPF AS L
    LEFT JOIN (SELECT * FROM sap_lfa1 WHERE CAST(data ->> 'SPRAS' AS TEXT) = 'EN') AS R
    ON LTRIM(RTRIM(L.data ->> 'LIFNR')) = LTRIM(RTRIM(R.data ->> 'LIFNR'))
    """



    j8 = """
    DROP TABLE IF EXISTS J3_BSEG_BKPF_LFA1_SKAT;

    SELECT L.*, LTRIM(RTRIM(R.data ->> 'TXT50')) AS TXT50
    INTO J3_BSEG_BKPF_LFA1_SKAT
    FROM J2_BSEG_BKPF_LFA1 AS L
    LEFT JOIN (SELECT  * FROM sap_skat WHERE CAST(data ->> 'SPRAS' AS TEXT) = 'EN') AS R
    ON LTRIM(RTRIM(L.KTOPL)) = LTRIM(RTRIM(R.data ->> 'KTOPL'))
                   AND LTRIM(RTRIM(L.data ->> 'SAKNR')) = LTRIM(RTRIM(R.data ->> 'SAKNR'))
        """

    j9 = """
    DROP TABLE IF EXISTS distinctVarAPKey;

    SELECT CONCAT(L.data ->> 'BUKRS', '_', L.data ->> 'BELNR', '_', L.data ->> 'GJAHR') AS varAPKey
    INTO distinctVarAPKey
    FROM sap_bseg AS L
    WHERE cast(L.data ->> 'KOART' as text) = 'K'
    GROUP BY L.data ->> 'BUKRS', L.data ->> 'BELNR', L.data ->> 'GJAHR'
        """

    j10 = """
    DROP TABLE IF EXISTS J4_BSEG_BKPF_LFA1_SKAT_OnlyAP;

    SELECT L.*
    INTO J4_BSEG_BKPF_LFA1_SKAT_OnlyAP
    FROM J3_BSEG_BKPF_LFA1_SKAT AS L
    INNER JOIN distinctVarAPKey AS R
    ON L.varAPKey = R.varAPKey
    """

    j11 = """
    DROP TABLE IF EXISTS J5_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO;

    SELECT L.*, R.data ->> 'TXZ01' as TXZ01, R.data ->> 'MATNR' AS MATNR2
    INTO J5_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO
    FROM J4_BSEG_BKPF_LFA1_SKAT_OnlyAP AS L
    LEFT JOIN (SELECT * FROM sap_ekpo) AS R
    ON L.data ->> 'EBELN' = R.data ->> 'EBELN'
                   AND L.data ->> 'EBELP' = R.data ->> 'EBELP'
    """

    j12 = """
    DROP TABLE IF EXISTS J6_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT;

    SELECT L.*, R.data ->> 'MAKTX' as MAKTX
    INTO J6_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT
    FROM J5_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO AS L
    LEFT JOIN (SELECT * FROM sap_makt WHERE cast( data ->> 'SPRAS' as text) = 'EN') AS R
    ON L.MATNR2 = R.data ->> 'MATNR'
    """

    j13 = """
    DROP TABLE IF EXISTS J8_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR;

    SELECT L.*
    INTO J8_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR
    FROM J6_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT AS L
    LEFT JOIN (SELECT *, CONCAT(data ->> 'ZBUKR', '_', data ->> 'VBLNR', '_', data ->> 'GJAHR') AS varAPKey FROM sap_payr) AS R
    ON L.varAPKey = R.varAPKey
    """


    j14 = """
          DROP TABLE IF EXISTS J9_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT;

    SELECT L.*, R.data ->> 'KTEXT'
    INTO J9_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT
    FROM J8_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR AS L
    LEFT JOIN (select cast(data as json) from (SELECT distinct cast(data as text) FROM sap_cskt WHERE cast( data ->> 'SPRAS' as text) = 'EN')  R )AS R
    ON L.data ->> 'KOSTL' = R.data ->> 'KOSTL'
    """

    j15 = """
    DROP TABLE IF EXISTS J10_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT_T007;

    SELECT L.*, R.data ->> 'KALSM' as KALSM, R.data ->> 'TEXT1' as TEXT1
    INTO J10_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT_T007
    FROM J9_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT AS L
    LEFT JOIN (SELECT  * FROM sap_t007s WHERE LTRIM(RTRIM(cast(data ->> 'KALSM' as text))) = 'ZTAXCA' AND cast(data ->> 'SPRAS' as text) = 'EN') AS R
    ON L.data ->> 'MWSKZ' = R.data ->> 'MWSKZ'
    """


    ## WARNING: Not every client uses these document types consistently.
    j16 = """
    DROP TABLE IF EXISTS RAW;
    select *
    into RAW
    from J10_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT_T007
    where ltrim(rtrim(BLART)) in ('AN', 'FD', 'FP', 'FY', 'RE', 'RX', 'SA', 'GG', 'GP', 'VC', 'VT')
    """

    # j17 =====================================================================
    # Add a few of andy's extra fields
    # Add varLocAmt (signed)
    # Add varDocAmt (signed)
    # Add sel_acct
    # Add amounts (unsigned)
    # Sort by varapkey, then by varLocAmt
    j17 = """
    DROP TABLE IF EXISTS RAW_SIGNED;
    SELECT * ,
    CASE
        WHEN data ->> 'SHKZG' = 'S' THEN DMBTR
        WHEN data ->> 'SHKZG' = 'H' THEN -1*DMBTR
        ELSE 0
    END AS varLocAmt,
    CASE
        WHEN data ->> 'SHKZG' = 'S' THEN WRBTR
        WHEN data ->> 'SHKZG' = 'H' THEN -1*WRBTR
        ELSE 0
    END AS varDocAmt,
    CASE
        WHEN data ->> 'HKONT' IN ('4700000000','4720000000','4750000000','4770000000') THEN 'G'
        WHEN data ->> 'HKONT' IN ('4000000000','4000000002','4009000000','4009000002','4009000032','4020000000','4020000002', '4029000000', '4109000002', '4100000000', '4100000002', '4100000010', '4109000000', '4109000010', '4120000000', '4120000002', '4120000010', '4129000000', '4129000002', '4129000010', '4170000000', '4300000000', '4400000000', '4420000000', '4420000010', '4429000010', '4449900000', '4609000000', '4650000000', '4751300000') THEN 'A'
        ELSE ''
    END AS sel_acct
    INTO RAW_SIGNED
    FROM
    (SELECT *,
    CAST(data ->> 'WRBTR' as float) as WRBTR,
    CAST(data ->> 'PSWBT' as float) as PSWBT,
    CAST(data ->> 'DMBTR' as float) as DMBTR,
    CAST(data ->> 'DMBE2' as float) as DMBE2,
    CAST(data ->> 'RWBTR' as float) as RWBTR
     FROM RAW) as L ORDER BY varapkey, varLocAmt DESC;
    """

    # Based on sel_acct value, assign the varLocAmt to the right account "bin"
    # e.g. AP, GST, PST, etc.
    j18 = """
    DROP TABLE IF EXISTS RAW_SORTED_ACCT;
    SELECT
    *,
    CASE
        WHEN sel_acct = 'G' THEN varLocAmt
        ELSE 0
    END AS GST_HST,
    CASE
        WHEN sel_acct = 'A' THEN varLocAmt
        ELSE 0
    END AS AP_AMT,
    CASE
        WHEN sel_acct = 'P' THEN varLocAmt
        ELSE 0
    END AS PST,
    CASE
        WHEN sel_acct = 'P_SA' THEN varLocAmt
        ELSE 0
    END AS PST_SA,
    CASE
        WHEN sel_acct = 'Q' THEN varLocAmt
        ELSE 0
    END AS QST,
    CASE
        WHEN sel_acct = 'O' THEN varLocAmt
        ELSE 0
    END AS TAXES_OTHER
    INTO RAW_SORTED_ACCT FROM RAW_SIGNED;
    """

    # Define a table, 'transaction_info', with the unique transaction information
    # WARNING: THIS MAY NOT BE THE CORRECT WAY TO SIFT TRANSACTION INFO.
    j19 = """
        DROP TABLE IF EXISTS transaction_info;
        SELECT B.* INTO transaction_info FROM
        (SELECT varapkey, MAX(varLocAmt) as var_max FROM RAW_SORTED_ACCT GROUP BY varapkey) AS A
        inner join
        (SELECT * FROM RAW_SORTED_ACCT) as B on A.varapkey = B.varapkey AND B.varLocAmt = A.var_max;
        """

    j20 = """
        DROP TABLE IF EXISTS transaction_summary;
        SELECT
        varapkey,
        SUM(varLocAmt) as varTransAmt,
        SUM(varLocAmt) as varLocAmt_sum,
        SUM(varDocAmt) as varDocAmt_sum,
        SUM(AP_AMT) as AP_AMT_sum,
        SUM(GST_HST) as GST_HST_sum,
        SUM(PST) as PST_sum,
        SUM(PST_SA) as PST_SA_sum,
        SUM(QST) as QST_sum,
        SUM(TAXES_OTHER) as TAXES_OTHER_sum,
        COUNT(varapkey) as COUNT
        INTO transaction_summary FROM RAW_SORTED_ACCT GROUP BY varapkey ORDER BY varapkey;
        """

    j21 = """
        DROP TABLE IF EXISTS caps_table;
        SELECT A.*, B.varTransAmt, B.varLocAmt_sum, B.varDocAmt_sum, B.AP_AMT_sum, B.GST_HST_sum, B.PST_sum, B.PST_SA_sum, B.QST_sum,B.TAXES_OTHER_sum, B.count
        INTO caps_table
        FROM
        (SELECT * FROM transaction_info) AS A
        inner join
        (SELECT * FROM transaction_summary) as B on A.varapkey = B.varapkey ORDER BY varapkey;
        """

    # Execute the joins defined above.
    # execute(j1)
    # execute(j2)
    # execute(j3)
    # execute(j4)
    # execute(j5)
    # execute(j6)
    # execute(j7)
    # execute(j8)
    # execute(j9)
    # execute(j10)
    # execute(j11)
    # execute(j12)
    # execute(j13)
    # execute(j14)
    # execute(j15)
    # execute(j16)
    # execute(j17)
    # execute(j18)
    # execute(j19)
    # execute(j20)
    execute(j21)


    return jsonify(response), 200

#This is the check that needs to be done to see whether vardocamt and varlocamt net to 0. This is referring to GL netting to 0. Ask Andy for more details.
@sap_caps_gen.route('/aps_quality_check', methods=['GET'])
def aps_quality_check():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)

# see feature branch 72-aps_to_caps for more info
@sap_caps_gen.route('/APS_to_CAPS', methods=['GET'])
def aps_to_caps():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)
