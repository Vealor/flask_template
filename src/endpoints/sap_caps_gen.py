'''
sap_caps_gen endpoints
'''
import csv
import datetime
import json
import os
import re
import zipfile
import requests
from collections import Counter
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from os import path
from src.models import *
from config import *
from src.util import *
sap_caps_gen = Blueprint('sap_caps_gen', __name__)



def mapping_serializer(label):
    return {
        "script_label": label.script_labels,
        "mappings": [{"column_name": map.column_name, "table_name" : map.table_name} for map in label.cdm_label_data_mappings.all()]
    }

#This takes the source data, in the form of a zip file, located in caps_gen_raw, and unzips it into caps_gen_unzipped.
#The endpoint can go through nested folders/zips.
@sap_caps_gen.route('/unzipping', methods=['POST'])
def unzipping():
    response = {'status': 'ok', 'message': '', 'payload': {'files_skipped': []}}
    try:
        data = request.get_json()
        if not os.path.exists(os.path.join(str(data['project_id']))):
            os.mkdir(str(data['project_id']))
            folders = ['sap_data', 'caps_gen_unzipped', 'caps_gen_raw', 'caps_gen_master']
            for folder in folders:
                os.mkdir((os.path.join(str(data['project_id']), folder)))
        if not isinstance(data, dict):
            raise Exception('data is not a dict')
        request_types = {
            'project_id' : 'int',
            'file_name': 'str',
            'system': 'str'
        }
        validate_request_data(data, request_types)
        get_data(data, response)
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    response['message'] = ''
    response['payload'] = []
    return jsonify(response), 200

#MAPPING HAPPENS: The CDM labels + Data Mappings table needs to be populated. See db_refresh.sh
@sap_caps_gen.route('/build_master_tables', methods=['POST'])
def build_master_tables():
    response = {'status': 'ok', 'message': {}, 'payload': {}}
    try:
        data = request.get_json()
        mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
        list_tablenames = list(set([table['mappings'][0]['table_name'] for table in mapping]))

        for table in list_tablenames:
            table_results = {}
            table_files = []

            #Search for all files that match table
            for file in os.listdir(os.path.join(str(data['project_id']), 'caps_gen_unzipped')):
                if re.search(table, file):
                    if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
                        table_files.append(file)
            print(table_files)
            #Load & union files into one master table in memory
            wfd = open(os.path.join(str(data['project_id']), 'caps_gen_master', '{}_MASTER.txt'.format(table)), 'wb')
            for index, file in enumerate(table_files):
                if index == 0:
                    with open(os.path.join(str(data['project_id']), 'caps_gen_unzipped', file), 'r' ,encoding='utf-8-sig') as fd:
                        wfd.write(fd.read().encode())
                else:
                    # for all future files
                    with open(os.path.join(str(data['project_id']), 'caps_gen_unzipped', file), 'r', encoding='utf-8-sig') as fd:
                        #   strip header
                        next(fd)
                        wfd.write(fd.read().encode())
            wfd.close()

            #initialize variables for bulk insertion
            referenceclass = eval('Sap' + str(table.lower().capitalize()))
            bulk_insert_handler = []

            #bulk insert into database
            with open(os.path.join(str(data['project_id']), 'caps_gen_master', '{}_MASTER.txt'.format(table)), 'r', encoding='utf-8-sig') as masterfile:
                counter = 0
                for line in csv.DictReader((line.replace('#|#', 'ø') for line in masterfile), delimiter='ø', quoting=csv.QUOTE_NONE):
                    counter += 1
                    if counter > 1000:
                        break
                    dict_to_insert = {'data' : line}
                    # WARNING: Project id needs to be provided in curl request
                    dict_to_insert['project_id'] = str(data['project_id'])
                    bulk_insert_handler.append(dict_to_insert)
            db.session.bulk_insert_mappings(referenceclass, bulk_insert_handler)
            db.session.commit()
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    response['message'] = ''
    response['payload'] = []
    return jsonify(response), 200

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
    response = {'status': 'ok', 'message': {}, 'payload': []}
    response.update({'renaming': {'status': 'ok', 'message': '', 'payload': []}})
    try:
        mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
        list_tablenames = list(set([table['mappings'][0]['table_name'] for table in mapping]))
        for table in list_tablenames:
            print(table)
            renamed_columndata = []
            rename_scheme = {}
            errorlines = []
            for index, elem in enumerate(mapping):
                if mapping[index]['mappings'][0]['table_name'] == table:
                    rename_scheme.update({mapping[index]['mappings'][0]['column_name']: mapping[index]['script_label']})
            print(rename_scheme)
            tableclass = eval('Sap' + str(table.lower().capitalize()))
            columndata = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).all()
            print(len(columndata))
            for row in columndata:
                row = rename_query_serializer(row)
                print(rename_scheme.values())
                print(row.keys())
                if [x for x in rename_scheme.values() if x in row['data'].keys()]:
                    [response.pop(key) for key in ['renaming']]
                    raise Exception('Your table has already been renamed. Please ensure that mapping has not been applied twice.')
                try:
                    #slow solution
                    for key, value in rename_scheme.items():
                        row['data'][value] = row['data'].pop(key)
                    renamed_columndata.append(row)
                except Exception as e:
                    errorlines.append(['Error in row' + str(row['id']), 'Error in Column ' + str(e), 'Table '  + str(table)])
            response['renaming']['payload'] = errorlines
            if len(response['renaming']['payload']) > 1:
                response['renaming']['message'] = 'Issue with the following lines. Check if column exists in source data or is populated appropriately in data dictionary'
                response['renaming']['status'] = 'error'
                raise Exception(response['renaming'])
            db.session.bulk_update_mappings(tableclass, renamed_columndata)
            db.session.commit()
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        return jsonify(response), 400
    response['message'] = ''
    response['payload'] = []
    return jsonify(response), 200


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

    response = {'status': 'ok', 'message': {}, 'payload': []}
    data_dictionary_results = {}
    uniqueness_response = {}
    try:
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
                uniqueness_response['results'] = dups
                uniqueness_response['final_score'] = 100 - (len(dups)/tableclass.query.count())
                print(uniqueness_response['final_score'])
                data_dictionary_results[table] = {'uniqueness' : uniqueness_response}
            else:
                uniqueness_response['final_score'] = 100
                data_dictionary_results[table] = {'uniqueness': 100}
            ### validity check ###
            for column in compiled_data_dictionary.keys():
                print(column)
                query = tableclass.query
                query = query.with_entities(getattr(tableclass, 'data')).all()
                query = [regex_serializer(row)['data'][column] for row in query]
                if compiled_data_dictionary[column]['regex']:
                    data_dictionary_results[table][column] = {
                        'regex': validity_check(query, compiled_data_dictionary[column]['regex'])}
        response['message'] = ''
        response['payload'] = data_dictionary_results
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return jsonify(response), 200

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
    try:

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

    # Execute the joins defined above.
        execute(j1)
        execute(j2)
        execute(j3)
        execute(j4)
        execute(j5)
        execute(j6)
        execute(j7)
        execute(j8)
        execute(j9)
        execute(j10)
        execute(j11)
        execute(j12)
        execute(j13)
        execute(j14)
        execute(j15)
        execute(j16)
        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
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
    def execute(query):
        print(str(datetime.datetime.now()))
        print("Executing...")
        result = db.session.execute(query)
        print("Committing...")
        db.session.commit()
        print("Done.")
        return 'query execute successful'

    try:
        response = {'status': 'ok', 'message': {}, 'payload': {}}
        j17 = """
            DROP TABLE IF EXISTS raw_relational;
            select
            CAST( data ->> 'MANDT' as TEXT) MANDT,
            CAST( data ->> 'SGTXT' as TEXT) SGTXT,
            CAST( data ->> 'BEWAR' as TEXT) BEWAR,
            CAST( data ->> 'KOART' as TEXT) KOART,
            CAST( data ->> 'BELNR' as TEXT) BELNR,
            CAST( data ->> 'REBZJ' as TEXT) REBZJ,
            CAST( data ->> 'KUNNR' as TEXT) KUNNR,
            CAST( data ->> 'GSBER' as TEXT) GSBER,
            CAST( data ->> 'ZBD1P' as TEXT) ZBD1P,
            CAST( data ->> 'MWSTS' as TEXT) MWSTS,
            CAST( data ->> 'SEGMENT' as TEXT) SEGMENT,
            CAST( data ->> 'VBUND' as TEXT) VBUND,
            CAST( data ->> 'STCEG' as TEXT) STCEG,
            CAST( data ->> 'XBILK' as TEXT) XBILK,
            CAST( data ->> 'HWBAS' as TEXT) HWBAS,
            CAST( data ->> 'SKFBT' as TEXT) SKFBT,
            CAST( data ->> 'EBELN' as TEXT) EBELN,
            CAST( data ->> 'ZUMSK' as TEXT) ZUMSK,
            CAST( data ->> 'ANBWA' as TEXT) ANBWA,
            CAST( data ->> 'BUZEI' as TEXT) BUZEI,
            CAST( data ->> 'ERFME' as TEXT) ERFME,
            CAST( data ->> 'ZFBDT' as TEXT) ZFBDT,
            CAST( data ->> 'VORGN' as TEXT) VORGN,
            CAST( data ->> 'GJAHR' as TEXT) GJAHR,
            CAST( data ->> 'XHKOM' as TEXT) XHKOM,
            CAST( data ->> 'ZBD3T' as TEXT) ZBD3T,
            CAST( data ->> 'KZBTR' as TEXT) KZBTR,
            CAST( data ->> 'FKBER_LONG' as TEXT) FKBER_LONG,
            CAST( data ->> 'BWKEY' as TEXT) BWKEY,
            CAST( data ->> 'AUGDT' as TEXT) AUGDT,
            CAST( data ->> 'ZBD2T' as TEXT) ZBD2T,
            CAST( data ->> 'AUGCP' as TEXT) AUGCP,
            CAST( data ->> 'HKONT' as TEXT) HKONT,
            CAST( data ->> 'ZUONR' as TEXT) ZUONR,
            CAST( data ->> 'PSWSL' as TEXT) PSWSL,
            CAST( data ->> 'XCPDD' as TEXT) XCPDD,
            CAST( data ->> 'ANLN2' as TEXT) ANLN2,
            CAST( data ->> 'AUFPL' as TEXT) AUFPL,
            CAST( data ->> 'XRAGL' as TEXT) XRAGL,
            CAST( data ->> 'KTOSL' as TEXT) KTOSL,
            CAST( data ->> 'KIDNO' as TEXT) KIDNO,
            CAST( data ->> 'VBEL2' as TEXT) VBEL2,
            CAST( data ->> 'XZAHL' as TEXT) XZAHL,
            CAST( data ->> 'DMBE2' as TEXT) DMBE2,
            CAST( data ->> 'ANLN1' as TEXT) ANLN1,
            CAST( data ->> 'NPLNR' as TEXT) NPLNR,
            CAST( data ->> 'APLZL' as TEXT) APLZL,
            CAST( data ->> 'REBZG' as TEXT) REBZG,
            CAST( data ->> 'SKNTO' as TEXT) SKNTO,
            CAST( data ->> 'AUGGJ' as TEXT) AUGGJ,
            CAST( data ->> 'PROJK' as TEXT) PROJK,
            CAST( data ->> 'MEINS' as TEXT) MEINS,
            CAST( data ->> 'XNEGP' as TEXT) XNEGP,
            CAST( data ->> 'HWMET' as TEXT) HWMET,
            CAST( data ->> 'PRCTR' as TEXT) PRCTR,
            CAST( data ->> 'SAKNR' as TEXT) SAKNR,
            CAST( data ->> 'QSSKZ' as TEXT) QSSKZ,
            CAST( data ->> 'WMWST' as TEXT) WMWST,
            CAST( data ->> 'MATNR' as TEXT) MATNR,
            CAST( data ->> 'ZBD1T' as TEXT) ZBD1T,
            CAST( data ->> 'BUZID' as TEXT) BUZID,
            CAST( data ->> 'FKBER' as TEXT) FKBER,
            CAST( data ->> 'TXGRP' as TEXT) TXGRP,
            CAST( data ->> 'KOSTL' as TEXT) KOSTL,
            CAST( data ->> 'SHKZG' as TEXT) SHKZG,
            CAST( data ->> 'ZTERM' as TEXT) ZTERM,
            CAST( data ->> 'XUMSW' as TEXT) XUMSW,
            CAST( data ->> 'XAUTO' as TEXT) XAUTO,
            CAST( data ->> 'AUGBL' as TEXT) AUGBL,
            CAST( data ->> 'UMSKS' as TEXT) UMSKS,
            CAST( data ->> 'VBELN' as TEXT) VBELN,
            CAST( data ->> 'BSCHL' as TEXT) BSCHL,
            CAST( data ->> 'BWTAR' as TEXT) BWTAR,
            CAST( data ->> 'QSFBT' as TEXT) QSFBT,
            CAST( data ->> 'WRBTR' as TEXT) WRBTR,
            CAST( data ->> 'MENGE' as TEXT) MENGE,
            CAST( data ->> 'REBZZ' as TEXT) REBZZ,
            CAST( data ->> 'TXJCD' as TEXT) TXJCD,
            CAST( data ->> 'PSWBT' as TEXT) PSWBT,
            CAST( data ->> 'TAXPS' as TEXT) TAXPS,
            CAST( data ->> 'MWSKZ' as TEXT) MWSKZ,
            CAST( data ->> 'PARGB' as TEXT) PARGB,
            CAST( data ->> 'ZLSCH' as TEXT) ZLSCH,
            CAST( data ->> 'WERKS' as TEXT) WERKS,
            CAST( data ->> 'BUKRS' as TEXT) BUKRS,
            CAST( data ->> 'AUFNR' as TEXT) AUFNR,
            CAST( data ->> 'DMBTR' as TEXT) DMBTR,
            CAST( data ->> 'QSSHB' as TEXT) QSSHB,
            CAST( data ->> 'BUSTW' as TEXT) BUSTW,
            CAST( data ->> 'EBELP' as TEXT) EBELP,
            CAST( data ->> 'UMSKZ' as TEXT) UMSKZ,
            CAST( data ->> 'GVTYP' as TEXT) GVTYP,
            CAST( data ->> 'ZBD2P' as TEXT) ZBD2P,
            CAST( data ->> 'NEBTR' as TEXT) NEBTR,
            CAST( data ->> 'EGLLD' as TEXT) EGLLD,
            case when cast(data ->> 'SHKZG' as TEXT) = 'H' 
                then -(cast(data ->> 'WRBTR' as FLOAT)) 
                else cast(data ->> 'WRBTR' as FLOAT) 
                end vardocamt,
            case when cast(data ->> 'SHKZG' as TEXT) = 'H' 
                then -(cast(data ->> 'DMBTR' as FLOAT)) 
                else  cast(data ->> 'DMBTR' as FLOAT) 
                end varlocamt,
            *
            into raw_relational
            from raw
        """


        #Generates raw account sum, groups varaccountcode and varapkey, sums on dmbtr, wrbtr, pswbt, dmbe2, vardocamt, and varlocamt. retrieves first row num for everything else. order by vartranamount
        j18 = """
        DROP TABLE IF EXISTS raw_acct_summ;
        SELECT
       *
       INTO raw_acct_summ
    FROM
       (
          SELECT
             Sum(Cast(dmbtr AS FLOAT)) AS DMBTR,
             Sum(Cast(wrbtr AS FLOAT)) AS WRBTR,
             Sum(Cast(pswbt AS FLOAT)) AS PSWBT,
             Sum(Cast(dmbe2 AS FLOAT)) AS DMBE2,
    	   SUM(vardocamt) as vardocamt,
    	   SUM(varlocamt) as varlocamt,

             l.varapkey,
             Trim(hkont) AS varaccountcode
          FROM
             raw_relational AS l
          GROUP BY
             varapkey,
             varaccountcode
       )
       AS l
       INNER JOIN
          (
             SELECT
                *
             FROM
                (
                SELECT
                varapkey as varapkey_temp,
                Trim(hkont) AS varaccountcode_temp,
                mandt,
                sgtxt,
                bewar,
                koart,
                belnr,
                rebzj,
                kunnr,
                gsber,
                zbd1p,
                mwsts,
                segment,
                vbund,
                stceg,
                xbilk,
                hwbas,
                skfbt,
                ebeln,
                zumsk,
                anbwa,
                buzei,
                erfme,
                zfbdt,
                vorgn,
                gjahr,
                xhkom,
                zbd3t,
                kzbtr,
                fkber_long,
                bwkey,
                augdt,
                zbd2t,
                augcp,
                hkont,
                zuonr,
                pswsl,
                xcpdd,
                anln2,
                aufpl,
                xragl,
                ktosl,
                kidno,
                vbel2,
                xzahl,
                anln1,
                nplnr,
                aplzl,
                rebzg,
                sknto,
                auggj,
                projk,
                meins,
                xnegp,
                hwmet,
                prctr,
                saknr,
                qsskz,
                wmwst,
                matnr,
                zbd1t,
                buzid,
                fkber,
                txgrp,
                kostl,
                shkzg,
                zterm,
                xumsw,
                xauto,
                augbl,
                umsks,
                vbeln,
                bschl,
                bwtar,
                qsfbt,
                menge,
                rebzz,
                txjcd,
                taxps,
                mwskz,
                pargb,
                zlsch,
                werks,
                bukrs,
                aufnr,
                qsshb,
                bustw,
                ebelp,
                umskz,
                gvtyp,
                zbd2p,
                nebtr,
                eglld,
                id,
                project_id,
                lifnr,
                varmultivnd,
                blart,
                bldat,
                xblnr,
                waers,
                monat,
                cputm,
                kursf,
                tcode,
                ktopl,
                name1,
                name2,
                land1,
                regio,
                ort01,
                pstlz,
                stras,
                txt50,
                txz01,
                matnr2,
                maktx,
                kalsm,
                Row_number() OVER( partition BY varapkey, Trim(hkont)
                ORDER BY
                mandt, 
                sgtxt, 
                bewar, 
                koart, 
                belnr,
                rebzj,
                kunnr,
                gsber,
                zbd1p,
                mwsts,
                segment,
                vbund,
                stceg,
                xbilk,
                hwbas,
                skfbt,
                ebeln,
                zumsk,
                anbwa,
                buzei,
                erfme,
                zfbdt,
                vorgn,
                gjahr,
                xhkom,
                zbd3t,
                kzbtr,
                fkber_long,
                bwkey,
                augdt,
                zbd2t,
                augcp,
                hkont,
                zuonr,
                pswsl,
                xcpdd,
                anln2,
                aufpl,
                xragl,
                ktosl,
                kidno,
                vbel2,
                xzahl,
                anln1,
                nplnr,
                aplzl,
                rebzg,
                sknto,
                auggj,
                projk,
                meins,
                xnegp,
                hwmet,
                prctr,
                saknr,
                qsskz,
                wmwst,
                matnr,
                zbd1t,
                buzid,
                fkber,
                txgrp,
                kostl,
                shkzg,
                zterm,
                xumsw,
                xauto,
                augbl,
                umsks,
                vbeln,
                bschl,
                bwtar,
                qsfbt,
                menge,
                rebzz,
                txjcd,
                taxps,
                mwskz,
                pargb,
                zlsch,
                werks,
                bukrs,
                aufnr,
                qsshb,
                bustw,
                ebelp,
                umskz,
                gvtyp,
                zbd2p,
                nebtr,
                eglld,
                id,
                project_id,
                lifnr,
                varmultivnd,
                blart,
                bldat,
                xblnr,
                waers,
                monat,
                cputm,
                kursf,
                tcode,
                ktopl,
                name1,
                name2,
                land1,
                regio,
                ort01,
                pstlz,
                stras,
                txt50,
                txz01,
                matnr2,
                maktx,
                kalsm,
                text1 DESC) AS roworder,
                   FROM
                      raw_relational
                )
                AS subq
             WHERE
                subq.roworder = 1
          )
          AS r
          ON l.varapkey = r.varapkey_temp
          AND l.varaccountcode = r.varaccountcode_temp
    	  order by varlocamt desc
          """


        j19 = """
        DROP TABLE IF EXISTS raw_tax_calc;
        select case when sel_acct = 'G' then varlocamt else 0 end as GST_HST ,
        case when sel_acct = 'P' then varlocamt else 0 end as PST,
        case when sel_acct = 'P_SA' then varlocamt else 0 end as PST_SA,
        case when sel_acct = 'O' then varlocamt else 0 end as TAXES_OTHER,
        case when sel_acct = 'Q' then varlocamt else 0 end as QST,
        case when sel_acct = 'A' then varlocamt else 0 end as AP_AMT,
        *
        into raw_tax_calc
        from (
        select
        case when varaccountcode in ('4700000000','4720000000','4750000000','4770000000') then 'G'
        when varaccountcode in ('NA') then 'P'
        when varaccountcode in ('NA') then 'P_SA'
        when varaccountcode in ('NA') then 'O'
        when varaccountcode in ('NA') then 'Q'
        when varaccountcode in ('4000000000',
        '4009000000',
        '4009000002',
        '4009000032',
        '4020000000',
        '4020000002',
        '4029000000',
        '4100000000',
        '4100000002',
        '4100000010',
        '4109000000',
        '4109000002',
        '4109000010',
        '4120000000',
        '4120000002',
        '4120000010',
        '4129000000',
        '4129000002',
        '4129000010',
        '4170000000',
        '4300000000',
        '4400000000',
        '4420000000',
        '4420000010',
        '4429000010',
        '4449900000',
        '4609000000',
        '4650000000',
        '4751300000'
        ) then 'A'
        else ''
        end as SEL_ACCT,
        	*
        from
        raw_acct_summ
        	) as subq
              """

        j20 = """
                  DROP TABLE IF EXISTS raw_summ;
        SELECT
           *
           INTO raw_summ
        FROM
           (
              SELECT
                 Sum(Cast(dmbtr AS FLOAT)) AS DMBTR,
                 Sum(Cast(wrbtr AS FLOAT)) AS WRBTR,
                 Sum(Cast(pswbt AS FLOAT)) AS PSWBT,
                 Sum(Cast(dmbe2 AS FLOAT)) AS DMBE2,
        	   SUM(vardocamt) as vardocamt,
        	   SUM(varlocamt) as vartranamount,
        	   SUM(varlocamt) as varlocamt,
        	   sum(AP_AMT) as AP_AMT,
        	   sum(GST_HST) as GST_HST,
        	   sum(PST) as PST,
        	   sum(PST_SA) as PST_SA,
        	   sum(QST) as QST,
        	   sum(TAXES_OTHER) as TAXES_OTHER,
                 varapkey
              FROM
                 raw_tax_calc
              GROUP BY
                 varapkey
           )
           AS l
           INNER JOIN
              (
                 SELECT
                    *
                 FROM
                    (
                       SELECT
                        varapkey as varapkey_temp,
                        mandt
                        sgtxt
                        bewar
                        koart
                        belnr
                        rebzj
                        kunnr
                        gsber
                        zbd1p
                        mwsts
                        segment
                        vbund
                        stceg
                        xbilk
                        hwbas
                        skfbt
                        ebeln
                        zumsk
                        anbwa
                        buzei
                        erfme
                        zfbdt
                        vorgn
                        gjahr
                        xhkom
                        zbd3t
                        kzbtr
                        fkber_long
                        bwkey
                        augdt
                        zbd2t
                        augcp
                        hkont
                        zuonr
                        pswsl
                        xcpdd
                        anln2
                        aufpl
                        xragl
                        ktosl
                        kidno
                        vbel2
                        xzahl
                        anln1
                        nplnr
                        aplzl
                        rebzg
                        sknto
                        auggj
                        projk
                        meins
                        xnegp
                        hwmet
                        prctr
                        saknr
                        qsskz
                        wmwst
                        matnr
                        zbd1t
                        buzid
                        fkber
                        txgrp
                        kostl
                        shkzg
                        zterm
                        xumsw
                        xauto
                        augbl
                        umsks
                        vbeln
                        bschl
                        bwtar
                        qsfbt
                        menge
                        rebzz
                        txjcd
                        taxps
                        mwskz
                        pargb
                        zlsch
                        werks
                        bukrs
                        aufnr
                        qsshb
                        bustw
                        ebelp
                        umskz
                        gvtyp
                        zbd2p
                        nebtr
                        eglld
                        id
                        project_id
                        lifnr
                        varmultivnd
                        blart
                        bldat
                        xblnr
                        waers
                        monat
                        cputm
                        kursf
                        tcode
                        ktopl
                        name1
                        name2
                        land1
                        regio
                        ort01
                        pstlz
                        stras
                        txt50
                        txz01
                        matnr2
                        maktx
                        kalsm

        				      Row_number() OVER( partition BY varapkey
                       ORDER BY
        				mandt
                        sgtxt
                        bewar
                        koart
                        belnr
                        rebzj
                        kunnr
                        gsber
                        zbd1p
                        mwsts
                        segment
                        vbund
                        stceg
                        xbilk
                        hwbas
                        skfbt
                        ebeln
                        zumsk
                        anbwa
                        buzei
                        erfme
                        zfbdt
                        vorgn
                        gjahr
                        xhkom
                        zbd3t
                        kzbtr
                        fkber_long
                        bwkey
                        augdt
                        zbd2t
                        augcp
                        hkont
                        zuonr
                        pswsl
                        xcpdd
                        anln2
                        aufpl
                        xragl
                        ktosl
                        kidno
                        vbel2
                        xzahl
                        anln1
                        nplnr
                        aplzl
                        rebzg
                        sknto
                        auggj
                        projk
                        meins
                        xnegp
                        hwmet
                        prctr
                        saknr
                        qsskz
                        wmwst
                        matnr
                        zbd1t
                        buzid
                        fkber
                        txgrp
                        kostl
                        shkzg
                        zterm
                        xumsw
                        xauto
                        augbl
                        umsks
                        vbeln
                        bschl
                        bwtar
                        qsfbt
                        menge
                        rebzz
                        txjcd
                        taxps
                        mwskz
                        pargb
                        zlsch
                        werks
                        bukrs
                        aufnr
                        qsshb
                        bustw
                        ebelp
                        umskz
                        gvtyp
                        zbd2p
                        nebtr
                        eglld
                        id
                        project_id
                        lifnr
                        varmultivnd
                        blart
                        bldat
                        xblnr
                        waers
                        monat
                        cputm
                        kursf
                        tcode
                        ktopl
                        name1
                        name2
                        land1
                        regio
                        ort01
                        pstlz
                        stras
                        txt50
                        txz01
                        matnr2
                        maktx
                        kalsm
                           DESC) AS roworder
        									   FROM
                          raw_tax_calc
                    )
                    AS subq
                 WHERE
                    subq.roworder = 1
              )
              AS r
              ON l.varapkey = r.varapkey_temp

        	  order by varlocamt desc
              """

        j21 = """
        select
        case when
         AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_PEI_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_PEI_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_PEI_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_PEI_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_BC_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_BC_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_BC_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_BC_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_SASK_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_SASK_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_SASK_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_SASK_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_ORST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_ORST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_ORST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_ORST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_QST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_QST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_QST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_QST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         when AP_AMT <> 0 and (SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 2, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 3, 3) = '000' or SUBSTRING(split_part(cast(EVEN_GST_RATE as text), '.', 2), 1, 3) = '999' ) then 'Y'
         else 'F'
         end
         EVEN_GST_IND,
         * from (
        select
        CASE WHEN
        EFF_RATE >= 6.9800000  and EFF_RATE <= 7.0999999 and New_Rate_Ind = 'A' then 'F'
        when EFF_RATE >= 5.9800000  and  EFF_RATE <= 6.0999999 and New_Rate_Ind = 'B' then 'F'
        when EFF_RATE >= 4.9800000  and  EFF_RATE <= 5.0999999 and (New_Rate_Ind = 'C' or New_Rate_Ind = 'D') then 'F'
        when EFF_RATE >= 14.9800000 and  EFF_RATE <= 15.949999 and New_Rate_Ind = 'A' then 'F'
        when EFF_RATE >= 13.9800000 and  EFF_RATE <= 14.949999  and New_Rate_Ind = 'B' then 'F'
        when EFF_RATE >= 12.9800000 and  EFF_RATE <= 13.949999  and New_Rate_Ind = 'C' then 'F'
        when EFF_RATE >= 11.9800000 and  EFF_RATE <= 12.099999  and New_Rate_Ind = 'D' then 'F'
        when EFF_RATE >= 12.9800000 and  EFF_RATE <= 13.099999  and New_Rate_Ind = 'D' then 'F'
        when EFF_RATE = 0.000000000 then 'F'
        else 'T' end ODD_IND,

        --calculation for prov tax ind PROV_TAX_IND <> '         '  'F'

        case when ABS(GST_HST) > 0 then 1 else 0 end GST_COUNT,

        case
        when EFF_RATE >= 6.980000  and  EFF_RATE <= 7.099999 then 'T'
        when EFF_RATE >= 5.980000  and  EFF_RATE <= 6.099999 then 'T'
        when EFF_RATE >= 4.980000  and  EFF_RATE <= 5.099999 then 'T'
        when EFF_RATE >= 14.980000 and  EFF_RATE <= 15.950000 then 'T'
        when EFF_RATE >= 13.980000 and  EFF_RATE <= 14.950000 then 'T'
        when EFF_RATE >= 12.980000 and  EFF_RATE <= 13.950000 then 'T'
        when EFF_RATE >= 11.980000 and  EFF_RATE <= 12.950000 then 'T'
        else 'F' end CN_FLAG_IND,

        case when EFF_RATE >= 14.980000 and EFF_RATE <= 15.950000 then 'T'
        else 'F' end CN_REP2_IND,
        --prov_ap code to be added
        case when
        PROV_TAX_IND = '' and GST_HST = 0 then ABS(AP_AMT*7.0000000000)/107.0000000000
         when PROV_TAX_IND = '' and GST_HST = 0 then ABS(AP_AMT*6.0000000000)/106.0000000000
         when PROV_TAX_IND = '' and GST_HST = 0 then  ABS(AP_AMT*5.0000000000)/105.0000000000
        when PROV_TAX_IND = '' and GST_HST = 0 then  ABS(AP_AMT*12.0000000000)/112.0000000000
        else 0.5555555555 end EVEN_GST_RATE,

        case when
         New_Rate_Ind = 'A' and PROV_TAX_IND = '' and GST_HST = 0 or PROV_TAX_IND = 'PEI-GST 7%'  then ABS(AP_AMT*7.0000000000)/117.7000000000
         when (New_Rate_Ind = 'B' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'PEI-GST 6%' then ABS(AP_AMT*6.0000000000)/116.6000000000
        when ((New_Rate_Ind = 'C' or New_Rate_Ind = 'D') and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'PEI-GST 5%' then  ABS(AP_AMT*5.0000000000)/115.5000000000
         else 0.5555555555 end EVEN_GST_PEI_RATE,

        case when
          (New_Rate_Ind = 'A' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'BC 7.5%-GST 7%' then ABS(AP_AMT*7.0000000000)/114.5000000000
         when  New_Rate_Ind = 'A' and PROV_TAX_IND = '' and GST_HST = 0 or PROV_TAX_IND = 'BC-MAN-SASK 7%-GST 7%' then ABS(AP_AMT*7.0000000000)/114.0000000000
        when (New_Rate_Ind = 'B' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'BC-MAN-SASK 7%-GST 6%' then  ABS(AP_AMT*6.0000000000)/113.0000000000
        when (New_Rate_Ind = 'C' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'BC-MAN 7%-GST 5%' then  ABS(AP_AMT*5.0000000000)/112.0000000000
         else 0.5555555555 end EVEN_GST_BC_RATE,



        case when
        (New_Rate_Ind = 'A' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'SASK 6%-GST 7%' then  ABS(AP_AMT*7.0000000000)/113.0000000000
        when (New_Rate_Ind = 'B' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'SASK 5%-GST 6%' then ABS(AP_AMT*6.0000000000)/111.0000000000
        when ((New_Rate_Ind = 'C' or New_Rate_Ind = 'D') and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'SASK 5%-GST 5%' then  ABS(AP_AMT*5.0000000000)/110.0000000000
        else  0.5555555555
        end EVEN_GST_SASK_RATE,

        case when
        (New_Rate_Ind = 'A' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'ORST-GST 7%' then ABS(AP_AMT*7.0000000000)/115.0000000000
        when (New_Rate_Ind = 'B' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'ORST-GST 6%' then  ABS(AP_AMT*6.0000000000)/114.0000000000
        when (New_Rate_Ind = 'C' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'ORST-GST 5%' then ABS(AP_AMT*5.0000000000)/113.0000000000
        else  0.5555555555 end EVEN_GST_ORST_RATE,

        case when
        New_Rate_Ind = 'A' and PROV_TAX_IND = '' and GST_HST = 0 or PROV_TAX_IND = 'QST 6.48%-GST 7%' then ABS(AP_AMT*7.0000000000)/115.0250000000
        when (New_Rate_Ind = 'B' and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'QST 6.48%-GST 6%' then ABS(AP_AMT*6.0000000000)/113.9500000000
        when ((New_Rate_Ind = 'C' or New_Rate_Ind = 'D') and PROV_TAX_IND = '' and GST_HST = 0) or PROV_TAX_IND = 'QST 6.48%-GST 5%' then  ABS(AP_AMT*5.0000000000)/112.8750000000
        else 0.5555555555
        end EVEN_GST_QST_RATE,


         case when
         New_Rate_Ind = 'A' then (abs(AP_AMT) - (abs(GST_HST)/0.0700000000)) - abs(GST_HST)
         when New_Rate_Ind = 'B' then (abs(AP_AMT) - (abs(GST_HST)/0.0600000000)) - abs(GST_HST)
         when New_Rate_Ind = 'C' then (abs(AP_AMT) - (abs(GST_HST)/0.0500000000)) - abs(GST_HST)
         else 0.00
         end PST_MAT,

         case when
          (New_Rate_Ind = 'A' AND (GST_HST < 0)) then (((abs(AP_AMT)-abs(PST)) * (7.0000000000/107.0000000000)) - abs(GST_HST)) * -1
         when (New_Rate_Ind = 'B' AND (GST_HST < 0)) then (((abs(AP_AMT)-abs(PST)) * (6.0000000000/106.0000000000)) - abs(GST_HST)) * -1
         when (New_Rate_Ind = 'C' AND (GST_HST < 0)) then (((abs(AP_AMT)-abs(PST)) * (5.0000000000/105.0000000000)) - abs(GST_HST)) * -1
          when (New_Rate_Ind = 'D' AND (GST_HST < 0)) then (((abs(AP_AMT)-abs(PST)) * (12.0000000000/112.0000000000)) - abs(GST_HST)) * -1
        when New_Rate_Ind = 'A' then  (((abs(AP_AMT)-abs(PST)) * (7.0000000000/107.0000000000)) - abs(GST_HST))
         when  New_Rate_Ind = 'B' then (((abs(AP_AMT)-abs(PST)) * (6.0000000000/106.0000000000)) - abs(GST_HST))
          when New_Rate_Ind = 'C' then (((abs(AP_AMT)-abs(PST)) * (5.0000000000/105.0000000000)) - abs(GST_HST))
         when New_Rate_Ind = 'D' then  (((abs(AP_AMT)-abs(PST)) * (12.0000000000/112.0000000000)) - abs(GST_HST))
         else 0.00
         end GST_MAT,

         case when
         New_Rate_Ind = 'A' then (abs(AP_AMT) - (abs(GST_HST)/0.0700000000))
        when New_Rate_Ind = 'B' then  (abs(AP_AMT) - (abs(GST_HST)/0.0600000000))
         when  New_Rate_Ind = 'C' then (abs(AP_AMT) - (abs(GST_HST)/0.0500000000))
         when New_Rate_Ind = 'D' then  (abs(AP_AMT) - (abs(GST_HST)/0.1200000000))
         else 0.00
         end BROKER_VALUE,



        case when
        AP_AMT = 0 then 0.00000
        else
         ((abs(GST_HST)*10000000)/(abs(AP_AMT)*100000))
        end
        BROKER_PCT,
        	 *
        from
        (
        select
        case when
        EFF_RATE >= 5.4235000 and eff_rate <= 5.4265000 and new_rate_ind = 'B' then  'PEI-GST 6%'
        when EFF_RATE >= 4.5233869 and eff_rate <= 4.5263869 and new_rate_ind ='C' or New_rate_ind = 'D' then  'PEI-GST 5%'
        when EFF_RATE >= 5.606000 AND EFF_RATE <= 5.6090000 and New_Rate_Ind = 'B' then  'BC-MAN-SASK 7%-GST 6%'
        when EFF_RATE >= 4.6713972 AND EFF_RATE <= 4.6743972 and (New_Rate_Ind = 'C' or New_Rate_Ind = 'D') then  'BC-MAN 7%-GST 5%'
        when EFF_RATE >= 5.7127000 AND EFF_RATE <= 5.7160000 and New_Rate_Ind = 'B' then 'SASK 5%-GST 6%'
        when EFF_RATE >= 4.7604048 AND EFF_RATE <= 4.7634048 and (New_Rate_Ind = 'C' or New_Rate_Ind = 'D') then  'SASK 5%-GST 5%'
        when EFF_RATE >= 5.5540000 AND EFF_RATE <= 5.5569990 and New_Rate_Ind = 'B' then  'ORST-GST 6%'
        when EFF_RATE >= 4.6281296 AND EFF_RATE <= 4.6311296 and (New_Rate_Ind = 'C' or New_Rate_Ind = 'D') then  'ORST-GST 5%'
        when EFF_RATE >= 5.5570000 AND EFF_RATE <= 5.5600000 and extract(year from cast(BLDAT as date)) <= 2007 then  'QST 6.48%-GST 6%'
        when EFF_RATE >= 4.6334942 AND EFF_RATE <= 4.6364942 and extract(year from cast(BLDAT as date)) < 2010  and extract(month from cast(BLDAT as date)) < 12 then  'QST 6.48%-GST 5%'
        when EFF_RATE >= 7.8720000 AND EFF_RATE <= 7.8780000 and extract(year from cast(BLDAT as date)) = 2010 and extract(month from cast(BLDAT as date)) <= 12 then  'QST 7.50%-GST 5%'
        when EFF_RATE >= 8.9220000 AND EFF_RATE <= 8.9280000 and extract(year from cast(BLDAT as date)) =2011 and extract(month from cast(BLDAT as date))<=12 then  'QST 8.50%-GST 5%'
        when EFF_RATE >= 9.9720000 AND EFF_RATE <= 9.9780000 and extract(year from cast(BLDAT as date))=2012 and extract(month from cast(BLDAT as date)) <=12 then  'QST 9.50%-GST 5%'
        when EFF_RATE >= 9.9720000 AND EFF_RATE <= 9.9780000 and extract(year from cast(BLDAT as date))>=2013 then  'HST_Quebec'
        when EFF_RATE >= 7.4980190 AND EFF_RATE <= 7.5007180  then  'QST AS GST'
         else '' end PROV_TAX_IND,
         *
        from (
        select
        case when
        --should be GST_HST = 0, but some bug is preventing me from doing the proper calculation.
        --PostgreSQL cannot handle mixed data types, setting this from text to numeric
        net_value = 0 then '9999' else abs(round(cast(GST_HST*1000000/NET_VALUE as numeric), 6)) end EFF_RATE,
        	net_value,
        *
        from (
        select
        case when extract(year from cast(BLDAT as date)) = 2006 and extract(month from cast(BLDAT as date)) > 6 then 'B'
        when extract(year from cast(BLDAT as date)) = 2007  then 'B'
        when extract(year from cast(BLDAT as date)) = 2008  then 'C'
        when extract(year from cast(BLDAT as date)) = 2009  then 'C'
        when extract(year from cast(BLDAT as date)) = 2010 and extract(month from cast(BLDAT as date)) < 7 then 'C'
        when extract(year from cast(BLDAT as date)) = 2010 and extract(month from cast(BLDAT as date)) >= 7 then 'D'
        when extract(year from cast(BLDAT as date)) = 2011  then 'D'
        when extract(year from cast(BLDAT as date)) = 2012  then 'D'
        when extract(year from cast(BLDAT as date)) = 2013 and extract(month from cast(BLDAT as date)) < 4 then 'D'
        when extract(year from cast(BLDAT as date)) = 2013 and extract(month from cast(BLDAT as date)) >= 4 then 'C'
        when extract(year from cast(BLDAT as date)) >= 2014 then 'C'
        else 'A' end
        New_Rate_Ind,
        upper(trim(name1)) as New_Vend_Name,
        abs(AP_AMT) - abs(GST_HST) - abs(PST) as Net_Value,
        	*
        from raw_summ) subq) subq1 ) subq2 ) subq3
        """

        j22 = """
                select rtrim(concat(noitc_var,
					itc_var,
					noitr_var,
					Even_var,
					QC_var,
					P5_var,
					P6_var,
					P7_var,
					P8_var,
					PST_SA_var,
					APGST_var,
					ODD5113_var,
					ODD5114_var,
					ODD5115_var, GSTSeperate_var), ', ') transaction_attributes,
					caps_no_attributes.*
					--into caps_with_attributes
					from (
        select
        case when GST_HST = 0.00 then 'NoITC, ' else null end as noitc_var,
        case when GST_HST <> 0.00 then 'ITC, ' else null end itc_var,
        case when QST = 0.00 then 'NoITR, ' else null end noitr_var,
        --case when ITR <> 0.00 then 'ITR' else null end itr, TBD what is ITR?
        --case when TOTAL_GST_HST <> 0.00 then 'TotalITC<>0.00'  else null end  totalitcnot0,
        --case when TOTAL_GST_HST = 0.00 then 'TotalITC=0.00' else  null end totalitceq0,
        --case when TOTAL_QST <> 0.00 then 'TotalITR<>0.00' else null end totalitrnot0,
        --case when GST_PCT >= 60 then 'GST_PCT>=60' else null end gst_pctgr60,
        --case when GST_PCT >= 20 and GST_PCT < 60 then '60<GST_PCT>=20' else null end gst_pctgr20less60,
        --case when varCurrency = 'CAD' then 'CCY' else null end CCY,
        --case when varCurrency <> 'CAD' then 'FCY' else null end FCY,
        case when even_gst_ind = 'Y' and GST_HST = 0.00 and GST_HST <> 0.00 then 'Even, ' else null end Even_var,
        case when eff_rate >= 4.544987838 and eff_rate <= 4.547987838 then 'QC, ' else null end QC_var,
        case when eff_rate >= 4.7604048 and eff_rate <= 4.7634048
        		and extract(year from cast(BLDAT as date)) <= 2015
        		and extract(year from cast(BLDAT as date)) >= 2014
        		or (extract(year from cast(BLDAT as date)) = 2017
        			and
        		    extract(month from cast(BLDAT as date)) <= 3
        		   and
        			extract(day from cast(BLDAT as date)) <= 24
        		   )
        		then 'QC, '
        		else null
        		end P5_var,
        case when eff_rate >= 4.715481132
        		and eff_rate <= 4.718481132
        		and (extract(year from cast(bldat as date)) = 2017
        		and extract(month from cast(bldat as date)) >= 3
        		and extract(date from cast(bldat as date)) >= 24)
        		or
        		extract(year from cast(bldat as date)) >= 2018
        		then 'P6, '
        		else null
        		end P6_var,
        case when (eff_rate >= 4.6713972 and eff_rate <= 4.6743972)
        		and (
        			extract(year from cast(bldat as date)) <= 2015
        			and
        			extract(year from cast(bldat as date)) <= 2015
        			or
        			(
        			extract(year from cast(bldat as date)) = 2017
        			and
        			extract(month from cast(bldat as date)) <= 3
        			and
        			extract(day from cast(bldat as date)) < 24
        			)
        		)
        		then 'P7, '
        		else null
        		end P7_var,
        case when (eff_rate >= 4.6281296 and eff_rate <= 4.6311296)
        and (
        extract(year from cast(bldat as date)) <= 2015
        )
        and (
        extract(year from cast(bldat as date)) >= 2014
        )
        or (
        	extract(year from cast(bldat as date)) = 2017
        	and
        	extract(month from cast(bldat as date)) <= 3
        	and
        	extract(day from cast(bldat as date)) < 24
        	)
        then 'P8, '
        else null
        end P8_var,
        case when PST_SA <> 0 then 'PST_SA, ' else null end PST_SA_var,
        --case when vend_cntry = 'Canada' then 'CdnVend' else null end CdnVend,
        --case when vend_cntry <> 'Canada' then 'ForeignVend' else null end ForeignVend,
        case when eff_rate = '0.000000' then 'AP=GST, ' else null end APGST_var,
        case when (eff_rate >= 4.626629629630 and eff_rate <= 4.632629629630) and new_rate_ind = 'D' then 'ODD_5/113, ' else null end ODD5113_var,
        case when (eff_rate >= 4.584155963303 and eff_rate <= 4.590155963303) and new_rate_ind = 'D' then 'ODD_5/114, ' else null end ODD5114_var,
        case when (eff_rate >= 4.542454545455 and eff_rate <= 4.548454545455) and new_rate_ind = 'D' then 'ODD_5/115, ' else null end ODD5115_var,
        --case when ODD_IND = 'T' and (PST_IMM ='N' or GST_IMM = 'Y') then 'ODD_GST_IMM' else null end ODD_GST_IMM,
        --case when ODD_IND = 'T' and (PST_IMM ='N' or GST_IMM = 'N') then 'ODD' else null end ODD,
        case when AP_AMT = 0.00 and GST_HST <> 0.00 then 'GSTSeperate, ' else null end GSTSeperate_var,
        --EPD, Broker, GST, QST, NoGST, NoQST remaining
						varapkey
        from
        caps_no_attributes) transaction_attributes
inner join caps_no_attributes
on caps_no_attributes.varapkey = transaction_attributes.varapkey
        """
        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return jsonify(response), 200