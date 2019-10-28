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
from sqlalchemy import exists, desc
from src.util import *

sap_caps_gen = Blueprint('sap_caps_gen', __name__)

@sap_caps_gen.route('project_path_creation', methods=['POST'])
def file_path_creation():
    response = {'status': 'ok', 'message': '', 'payload': []}
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            raise Exception('data is not a dict')
        request_types = {
            'project_id': 'int',
            'system': 'str'
        }
        validate_request_data(data, request_types)
        if not os.path.exists(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']))):
            print('path does not exist, creating project')
            os.mkdir(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id'])))
            folders = ['sap_data', 'caps_gen_unzipped', 'caps_gen_raw', 'caps_gen_master']
            for folder in folders:
                os.mkdir((os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), folder)))
        else:
            raise Exception('Path has already been created for project')
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 200

#This takes the source data, in the form of a zip file, located in caps_gen_raw, and unzips it into caps_gen_unzipped.
#The endpoint can go through nested folders/zips.
@sap_caps_gen.route('/unzipping', methods=['POST'])
def unzipping():
    response = {'status': 'ok', 'message': '', 'payload': {'files_skipped': []}}
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            raise Exception('data is not a dict')
        request_types = {
            'project_id' : 'int',
            'file_name': 'str',
            'system': 'str'
        }
        validate_request_data(data, request_types)
        source_data_unzipper(data, response)
    except Exception as e:
        current_output_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
        list(map(os.unlink, (os.path.join(current_output_path, f) for f in os.listdir(current_output_path))))
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
    return jsonify(response), 200

#MAPPING HAPPENS: The CDM labels + Data Mappings table needs to be populated. See db_refresh.sh
@sap_caps_gen.route('/build_master_tables', methods=['POST'])
def build_master_tables():
    response = {'status': 'ok', 'message': {}, 'payload': {}}
    print('hello')
    try:
        data = request.get_json()
        # deletecheck = CapsGen.query.filter(CapsGen.project_id == data['project_id']).first()
        # if deletecheck:
        #     db.session.delete(deletecheck)
        #     db.session.commit()
        #capsgen = CapsGen(user_id=data['user_id'], project_id=data['project_id'], is_completed=False)
        #db.session.add(capsgen)
        #db.session.flush()

        list_tablenames = current_app.config['CDM_TABLES']
        list_tablenames = ['SKA1']
        #TODO: IF UNZIPPING FILES EXIST, DELETE THEM FIRST AND THEN START AGAIN
        for table in list_tablenames:
            print(table)
            table_files = []
            #Search for all files that match table
            for file in os.listdir(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])):
                if re.search(table, file):
                    if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
                        table_files.append(file)
            #Load & union files into one master table in memory
            wfd = open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_MASTER_LOCATION'], '{}_MASTER.txt'.format(table)), 'wb')
            for index, file in enumerate(table_files):
                if index == 0:
                    with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'], file), 'r' ,encoding='utf-8-sig') as fd:
                        wfd.write(fd.read().encode())
                else:
                    # for all future files
                    with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'], file), 'r', encoding='utf-8-sig') as fd:
                        #   strip header
                        next(fd)
                        wfd.write(fd.read().encode())
            wfd.close()

            #initialize variables for bulk insertion
            referenceclass = eval('Sap' + str(table.lower().capitalize()))
            bulk_insert_handler = []
            #bulk insert into database
            with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), 'caps_gen_master', '{}_MASTER.txt'.format(table)), 'r', encoding='utf-8-sig') as masterfile:
                counter = 0
                for line in csv.DictReader((line.replace('#|#', 'ø') for line in masterfile), delimiter='ø', quoting=csv.QUOTE_NONE):
                    #testing purposes only
                    # counter += 1
                    # if counter > 100000:
                    #     break
                    dict_to_insert = {'data' : line}
                    # WARNING: Project id needs to be provided in curl request
                    #modified capsgen id to be 9
                    dict_to_insert['capsgen_id'] = 9
                    bulk_insert_handler.append(dict_to_insert)
            db.session.bulk_insert_mappings(referenceclass, bulk_insert_handler)
            CapsGen.query.filter(CapsGen.project_id == data['project_id']).update({"is_completed": True})
            #converted db flush to commit because of memory issue
            db.session.commit()
        response['message'] = 'All tables are successfully committed.'
        #once back to flush, replace db.commit()
    except Exception as e:
        db.session.rollback()
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
@sap_caps_gen.route('/rename_scheme', methods=['POST'])
def rename_scheme():
    #TODO: CHECK IF PROJECT exists
    #TODO: RETURN ALL TABLES THAT FAIL INSTEAD OF ONE AT A TIME
    #jsonify DB query
    def rename_query_serializer(row):
        return {
            "id": row.id,
            "data": row.data
        }
    response = {'status': 'ok', 'message': {}, 'payload': []}
    response.update({'renaming': {'status': 'ok', 'message': '', 'payload': []}})
    try:
        data = request.get_json()
        mapping = [label.serialize for label in CDM_label.query.all()]
        list_tablenames = current_app.config['CDM_TABLES']
        list_tablenames = ['SKA1']
        for table in list_tablenames:
            print(table)
            renamed_columndata = []
            rename_scheme = {}
            columns_missing = []
            errorlines = []
            for index, elem in enumerate(mapping):
                if mapping[index]['mappings'][0]['table_name'] == table:
                    rename_scheme.update({mapping[index]['mappings'][0]['column_name']: mapping[index]['script_label']})
            tableclass = eval('Sap' + str(table.lower().capitalize()))
            columndata = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).filter(tableclass.capsgen_id == data['project_id']).all()
            for row in columndata:
                row = rename_query_serializer(row)
                if [x for x in rename_scheme.values() if x in row['data'].keys()]:
                    [response.pop(key) for key in ['renaming']]
                    raise Exception('Your table has already been renamed. Please ensure that mapping has not been applied twice.')
                for column in rename_scheme.keys():
                    if column not in list(row['data'].keys()):
                        columns_missing.append((str(table) + '-' + str(column)))
                if columns_missing:
                    response['renaming']['payload'] = columns_missing
                    raise ValueError('Columns are missing from data')
                try:
                    #slow solution
                    for key, value in rename_scheme.items():
                        row['data'][value] = row['data'].pop(key)
                    renamed_columndata.append(row)
                except Exception as e:
                    errorlines.append(['Error in row' + str(row['id']), 'Error in Column ' + str(e), 'Table '  + str(table)])
            print(errorlines)
            response['renaming']['payload'] = errorlines
            if len(response['renaming']['payload']) > 1: #CHANGE BACK TO 1
                response['renaming']['message'] = 'Issue with the following lines. Check if column exists in source data or is populated appropriately in data dictionary'
                response['renaming']['status'] = 'error'
                raise Exception(response['renaming'])
            db.session.bulk_update_mappings(tableclass, renamed_columndata)
            db.session.flush()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
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

    def validity_check(result, regex):
        validity_response = {}
        results = list(filter(re.compile(regex).match, result))
        validity_response['results'] = results
        validity_response['final_score'] = 100 - (len(validity_response['results'])/len(column))
        return validity_response

    def completeness_check(result):
        completeness_response = {}
        counter = 0
        results = [elem for elem in result if elem == '' or elem == None]
        completeness_response['final_score'] =  (len(results) / len(result)) * 100
        return completeness_response

    response = {'status': 'ok', 'message': {}, 'payload': []}
    data_dictionary_results = {}
    uniqueness_response = {}
    try:
        data = request.get_json()
        CDM_query = [label.serialize for label in CDM_label.query.all()]
        list_tablenames = list(set([table['mappings'][0]['table_name'] for table in CDM_query if table['mappings']]))
        for table in list_tablenames:
            data_dictionary_results[table] = {}
            tableclass = eval('Sap' + str(table.lower().capitalize()))
            compiled_data_dictionary = data_dictionary(CDM_query, table)
            data = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).filter(
                tableclass.capsgen_id == data['project_id']).all()
            ### UNIQUENESS CHECK ###
            #The argument should be set to true when some of is_unique column in CDM labels is set to True.
            unique_keys = [x for x in compiled_data_dictionary if compiled_data_dictionary[x]['is_unique'] == False]
            if unique_keys:
                unique_key_checker = []
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
                data_dictionary_results[table] = {'uniqueness' : uniqueness_response}
            else:
                uniqueness_response['final_score'] = 100
                data_dictionary_results[table] = {'uniqueness': 100}
            ### validity check ###
            for column in compiled_data_dictionary.keys():
                query = [regex_serializer(row)['data'][column] for row in data]
                if compiled_data_dictionary[column]['regex']:
                    data_dictionary_results[table][column] = {
                        'regex': validity_check(query, compiled_data_dictionary[column]['regex'])}
            ###completeness check ###
                data_dictionary_results[table][column] = {
                    'completeness': completeness_check(query)}
        response['message'] = ''
        response['payload'] = data_dictionary_results
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return jsonify(response), 200

#j1 to j10 joins to create APS
@sap_caps_gen.route('/j1_j10', methods=['POST'])
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
        data = request.get_json()
        #capsgen_id is max of the project id
        capsgen_id = CapsGen.query.filter(CapsGen.project_id == data['project_id']).order_by(desc(CapsGen.id)).first().id

        project = Project.find_by_id(data['project_id'])
        if not project:
            raise ValueError('Project id does not exist')

        if not capsgen_id:
            raise ValueError('Capsgen has not been run on this project yet. Please run Capsgen from source data upload.')
        print(capsgen_id)

        #Create varapkey for BKPF
        j1revised = """DROP TABLE IF EXISTS BKPF_VARAP_MSTR;
        select
        L.*,
        ltrim(rtrim(cast(L.data ->> 'bkpf_bukrs_key' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'bkpf_belnr_key' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'bkpf_gjahr_key' AS Text))) varapkey
        into BKPF_VARAP_MSTR
        from
        (select * from sap_bkpf where cast(data ->> 'bkpf_gjahr_key' as text) = '2013' and cast(data ->> 'fiscal_period_gl' as text) = '03' and capsgen_id = {capsgen_id}) as L
        """.format(capsgen_id = capsgen_id)
        print('it got here')

        #create varapkey for bseg
        j2revised = """
        DROP TABLE IF EXISTS BSEG_AP;
        select
        L.*,
        ltrim(rtrim(cast(L.data ->> 'co_code_gl' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'gl_doc_num' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'fiscal_year_gl' AS Text))) varAPKey,
        cast('' as text) AS varMultiVND,
        cast('' as text) as varSupplier_No
        into  BSEG_AP
        from (select * from sap_bseg where cast(data ->> 'fiscal_year_gl' as text) = '2013' and capsgen_id = {capsgen_id}) as L
        """.format(capsgen_id = capsgen_id)
        print('it got here')

        # Set the
        j3revised = """
        DROP TABLE IF EXISTS distinctVarAPKeyVendorAcctNum;
        SELECT DISTINCT L.varAPKey, LTRIM(RTRIM(L.data ->> 'vend_num')) AS vend_num, Row_Number() Over(Partition by varAPKey ORDER BY L.data ->> 'vend_num') AS RowNum
        INTO table distinctVarAPKeyVendorAcctNum
        FROM BSEG_AP AS L
        WHERE L.data ->> 'vend_num' IS NOT NULL
                       AND LTRIM(RTRIM(L.data ->> 'vend_num')) != ''
        """
        print('it got here')
        j4revised = """
        DROP TABLE IF EXISTS distinctVarAPKeyMultiVendor;
        SELECT varAPKey, COUNT(*) AS Cnt
        INTO table distinctVarAPKeyMultiVendor
        FROM distinctVarAPKeyVendorAcctNum AS L
        GROUP BY varAPKey
        HAVING COUNT(*) >  1
        """
#Update Vendor Account Number for each varAPKey if Vendor Account Number is null with the first vendor account number
        print('it got here')
        j5revised = """
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

        j6revised = """
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

        j7revised = """
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
        """.format(capsgen_id = capsgen_id)

        #SKA1 is missing BUKRS
        # j8revised = """
        # DROP TABLE IF EXISTS aps;
        #
        # SELECT L.*,
        # R.data as SKAT_data
        # INTO aps
        # FROM J2_BSEG_BKPF_LFA1 AS L
        # LEFT JOIN (SELECT  * FROM sap_skat WHERE CAST(data ->> 'skat_spras_key' AS TEXT) = 'EN' and capsgen_id = {capsgen_id}) AS R
        # ON LTRIM(RTRIM(L.data ->> 'largest_debit_half_acct_num_gl')) = LTRIM(RTRIM(R.data ->> 'skat_ktopl_key'))
        #                AND LTRIM(RTRIM(L.data ->> 'SAKNR')) = LTRIM(RTRIM(R.data ->> 'skat_saknr_key'))
        #     """.format(capsgen_id = capsgen_id)

        j9 = """
        DROP TABLE IF EXISTS distinctVarAPKey;

        SELECT CONCAT(L.data ->> 'co_code_gl', '_', L.data ->> 'gl_doc_num', '_', L.data ->> 'fiscal_year_gl') AS varAPKey
        INTO distinctVarAPKey
        FROM sap_bseg AS L
        WHERE cast(L.data ->> 'KOART' as text) = 'K' and capsgen_id = {capsgen_id}
        GROUP BY L.data ->> 'co_code_gl', L.data ->> 'gl_doc_num', L.data ->> 'fiscal_year_gl'
            """.format(capsgen_id = capsgen_id)

        j10 = """
        DROP TABLE IF EXISTS J3_BSEG_BKPF_LFA1_OnlyAP;

        SELECT L.*
        INTO J3_BSEG_BKPF_LFA1_OnlyAP
        FROM J2_BSEG_BKPF_LFA1 AS L
        INNER JOIN distinctVarAPKey AS R
        ON L.varAPKey = R.varAPKey
        """

    # Execute the joins defined above.
        execute(j1revised)
        execute(j2revised)
        execute(j3revised)
        execute(j4revised)
        execute(j5revised)
        execute(j6revised)
        execute(j7revised)
        execute(j8revised)
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
    try:
        response['VERSION'] = current_app.config['VERSION']
        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
        response['payload'] = []
        return jsonify(response), 400
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
        """.format(project_id = data['project_id'])

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
        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return jsonify(response), 200

def caps_to_erd_1():
    try:
        #Join TBSLT
        j16 = """
        drop table if exists caps_1;

        select   L.*,
        R.data ->> 'tbslt_bschl_key' as tbslt_bschl_key,
        R.data ->> 'post_key_descr' as post_key_descr,
        R.data ->> 'tbslt_umskz_key' as tbslt_umskz_key,
        R.data ->> 'tbslt_spras_key' as tbslt_spras_key
        into caps_1
        from caps as L
        left join (select * from sap_tbslt where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'post_key_gl' = R.data ->> 'tbslt_bschl_key'
        """
        #Join T001
        j17 = """
        drop table if exists caps_2;

        select   L.*,
        R.data ->> 'co_name' as co_name,
        R.data ->> 't001_land1_key' as t001_land1_key,
        R.data ->> 't001_bukrs_key' as t001_bukrs_key
        into caps_2
        from caps_1 as L
        left join (select * from sap_T001 where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'co_code_gl' = R.data ->> 't001_bukrs_key'
        """
        #Join T005S
        j18 = """
        drop table if exists caps_3;

        select   L.*,
        R.data ->> 't005s_bland_key' as t005s_bland_key,
        R.data ->> 'prov_tx_code_tx' as prov_tx_code_tx,
        R.data ->> 't005s_land1_key' as t005s_land1_key
        into caps_3
        from caps_2 as L
        left join (select * from sap_t005s where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'GRIRG' = R.data ->> 't005s_bland_key'
        """
        # #Join CSKS to CSKT
        # j19 = """
        # drop table if exists j1_csks_cskt;
        #
        # select L.data ->> 'csks_kokrs_key' as csks_kokrs_key,
        # L.data ->> 'csks_kostl_key' as csks_kostl_key,
        # L.data ->> 'csks_datbi_key' as csks_datbi_key,
        # L.data ->> 'cost_ctr_tx_jur' as cost_ctr_tx_jur,
        # R.data ->> 'cskt_spras_key' as cskt_spras_key,
        # R.data ->> 'cskt_kokrs_key' as cskt_kokrs_key,
        # R.data ->> 'cskt_datbi_key' as cskt_datbi_key,
        # R.data ->> 'cskt_kostl_key' as cskt_kostl_key,
        # R.data ->> 'cost_ctr_name' as cost_ctr_name,
        # R.data ->> 'cost_ctr_descr' as cost_ctr_descr
        # into j1_csks_cskt
        # from (select * from sap_csks where capsgen_id = {capsgen_id}) as L
        # left join (select * from sap_cskt where capsgen_id = {capsgen_id}) as R
        # on L.data ->> 'csks_kokrs_key' = R.data ->> 'cskt_kokrs_key'
        # and L.data ->> 'csks_kostl_key' = R.data ->> 'cskt_kostl_key'
        # """
        # #join CAPS to CSKS CSKT
        # j20 = """
        # drop table if exists caps_4;
        # select L.*,
        # R.*
        # into caps_4
        # from (select * from caps_3) as L
        # left join (select * from j1_csks_cskt) as R
        # on L.data ->> 'control_area_gl' = R.csks_kokrs_key
        # """
        # #join CEPC and CEPCT
        # j21 = """
        # drop table if exists j1_CEPC_CEPCT;
        # select
        # L.data ->> 'cepc_datbi_key' as cepc_datbi_key,
        # L.data ->> 'cepc_kokrs_key' as cepc_kokrs_key,
        # L.data ->> 'cepc_prctr_key' as cepc_prctr_key,
        # L.data ->> 'profit_ctr_tx_jur' as profit_ctr_tx_jur,
        # L.data ->> 'datab' as datab,
        # R.data ->> 'profit_ctr_name' as profit_ctr_name,
        # R.data ->> 'profit_ctr_descr' as profit_ctr_descr,
        # R.data ->> 'cepct_prctr_key' as cepct_prctr_key,
        # R.data ->> 'cepct_spras_key' as cepct_spras_key,
        # R.data ->> 'KOKRS' as KOKRS
        # into j1_CEPC_CEPCT
        # from (select * from sap_cepc where capsgen_id = {capsgen_id}) as L
        # left join (select * from sap_cepct where capsgen_id = {capsgen_id}) as R
        # on L.data ->> 'cepc_prctr_key' = R.data ->> 'cepct_prctr_key'
        # and L.data ->> 'cepc_kokrs_key' = R.data ->> 'KOKRS'
        # """
        # #join CAPS with j1_CEPC_CEPCT
        # j22 = """
        # drop table if exists caps_5;
        # select L.*,
        # R.*
        # into caps_5
        # from caps_4 as L
        # left join (select * from j1_CEPC_CEPCT) as R
        # on L.data ->> 'profit_ctr_num' = R.cepc_prctr_key
        # and L.data ->> 'bseg_budat_key' = R.cepc_datbi_key
        #"""

        j23 = """
        drop table if exists j1_PRPS_PROJ;
        select
        L.data ->> 'object_num_proj' as object_num_proj,
        L.data ->> 'jv_obj_type_proj' as jv_obj_type_proj,
        L.data ->> 'wbs_bus_area_proj' as wbs_bus_area_proj,
        L.data ->> 'wbs_cntrl_area_proj' as wbs_cntrl_area_proj,
        L.data ->> 'wbs_elem_id_proj' as wbs_elem_id_proj,
        L.data ->> 'wbs_elem_descr_proj' as wbs_elem_descr_proj,
        L.data ->> 'proj_type_proj' as proj_type_proj,
        L.data ->> 'prps_psphi_key' as prps_psphi_key,
        L.data ->> 'prps_pspnr_key' as prps_pspnr_key,
        L.data ->> 'proj_loc_proj' as proj_loc_proj,
        L.data ->> 'ETYPE' as prps_etype_key,
        L.data ->> 'FKBER' as prps_fkber_key,
        L.data ->> 'PBUKR' as prps_pbukr_key,
        L.data ->> 'PRCTR' as prps_prctr_key,
        L.data ->> 'RECID' as prps_recid_key,
        R.data ->> 'proj_descr_proj' as proj_descr_proj,
        R.data ->> 'proj_defin_proj' as proj_defin_proj,
        R.data ->> 'proj_internal_proj' as proj_internal_proj,
        R.data ->> 'proj_tx_jur_proj' as proj_tx_jur_proj,
        R.data ->> 'proj_mngr_name_proj' as proj_mngr_name_proj,
        R.data ->> 'proj_mngr_num_proj' as proj_mngr_num_proj,
        R.data ->> 'bus_area_proj' as bus_area_proj,
        R.data ->> 'plant_proj' as plant_proj,
        R.data ->> 'KOSTL' as proj_kostl_key,
        R.data ->> 'PRCTR' as proj_prctr_key
        into j1_PRPS_PROJ
        from (select * from sap_prps where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_proj where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'prps_psphi_key' = R.data ->> 'proj_internal_proj'
        """

        j24 = """
        drop table if exists j2_PRPS_PROJ_TTXJT;
        select L.*,
        R.data ->> 'ttxjt_spras_key' as ttxjt_spras_key,
        R.data ->> 'ttxjt_kalsm_key' as ttxjt_kalsm_key,
        R.data ->> 'tx_jur_descr_tx' as tx_jur_descr_tx,
        R.data ->> 'ttxjt_txjcd_key' as ttxjt_txjcd_key
        into j2_PRPS_PROJ_TTXJT
        from j1_PRPS_PROJ as L
        left join (select * from sap_ttxjt where capsgen_id = {capsgen_id}) as R
        on L.proj_tx_jur_proj = R.data ->> 'ttxjt_txjcd_key'
        """

        j25 = """
        drop table if exists j3_PRPS_PROJ_TTXJT_T001W;
        select L.*,
        R.data ->> 'plant_name_plant' as plant_name_plant,
        R.data ->> 'plant_tx_jur_plant' as plant_tx_jur_plant,
        R.data ->> 't001w_werks_key' as t001w_werks_key
        into j3_PRPS_PROJ_TTXJT_T001W
        from j2_PRPS_PROJ_TTXJT as L
        left join (select * from sap_t001w where capsgen_id = {capsgen_id}) as R
        on L.plant_proj = R.data ->> 't001w_werks_key'
        """

        j26 = """
        drop table if exists caps_4;
        select L.*,
        R.*
        into caps_4
        from caps_3 as L
        left join j3_PRPS_PROJ_TTXJT_T001W as R
        on L.data ->> 'wbs_gl' = R.prps_pspnr_key
        """

        # j27 = """
        # drop table if exists j1_T007A_T007S;
        # select
        # L.data ->> 't007a_kalsm_key' as t007a_kalsm_key,
        # L.data ->> 't007a_mwskz_key' as t007a_mwskz_key,
        # R.data ->> 't007s_kalsm_key' as t007s_kalsm_key,
        # R.data ->> 't007s_mwskz_key' as t007s_mwskz_key,
        # R.data ->> 't007s_spras_key' as t007s_spras_key,
        # R.data ->> 'tx_name_tx' as tx_name_tx
        # into j1_T007A_T007S
        # from (select * from sap_t007a where capsgen_id = {capsgen_id}) as L
        # left join (select * from sap_t007s where capsgen_id = {capsgen_id}) as R
        # on L.data ->> 't007a_kalsm_key' = R.data ->> 't007s_kalsm_key'
        # and
        # L.data ->> 't007a_mwskz_key' = R.data ->> 't007s_mwskz_key'
        # """
        # #Join CAPS to T007A T007S
        # j28 = """
        # drop table if exists caps_12;
        # select L.*,
        # R.*
        # into caps_12
        # from caps_11 as L
        # left join j1_T007A_T007S as R
        # on L.data ->> 'bseg_mwsk3_key' = R.t007s_mwskz_key
        # """
        #Join caps to TTXJT
        j29 = """
        drop table if exists caps_5;
        select L.*,
        R.data ->> 'ttxjt_kalsm_key' as ttxjt_kalsm_key
        R.data ->> 'ttxjt_spras_key' as ttxjt_spras_key
        R.data ->> 'tx_jur_descr_tx' as tx_jur_descr_tx
        R.data ->> 'ttxjt_txjcd_key' as ttxjt_txjcd_key
        into caps_5
        from caps_4 as L
        left join (select * from sap_ttxjt where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'tax_jur_gl' = R.data ->> 'ttxjt_txjcd_key'
        """.format(capsgen_id = capsgen_id)
        #Join SKA1 to SKAT
        # j30 = """
        # drop table if exists J1_SKA1_SKAT;
        # select L.data ->> 'ska1_bukrs_key' as ska1_bukrs_key,
        # L.data ->> 'ska1_ktopl_key' as ska1_ktopl_key,
        # L.data ->> 'ska1_saknr_key' as ska1_saknr_key,
        # R.data ->> 'skat_spras_key' as skat_spras_key,
        # R.data ->> 'skat_ktopl_key' as skat_ktopl_key,
		# R.data ->> 'skat_saknr_key' as skat_saknr_key,
        # R.data ->> 'lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl' as lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl
        # into j1_SKA1_SKAT
        # from (select * from sap_ska1 where capsgen_id = {capsgen_id}) as L
        # left join (select * from sap_skat where capsgen_id = {capsgen_id}) as R
        # on L.data ->> 'ska1_ktopl_key' = R.data ->> 'skat_ktopl_key'
        # and
        # L.data ->> 'ska1_saknr_key' = R.data ->> 'skat_saknr_key'
        # """
        #
        # j31 = """
        # drop table if exists J2_SKB1_SKA1_SKAT;
        # select L.data ->> 'skb1_bukrs_key' as skb1_bukrs_key,
        # L.data ->> 'skb1_saknr_key' as skb1_saknr_key,
        # R.*
        # into J2_SKB1_SKA1_SKAT
        # from (select * from sap_skb1 where capsgen_id = {capsgen_id}) as L
        # left join J1_SKA1_SKAT as R
        # on L.data ->> 'skb1_bukrs_key' = R.ska1_bukrs_key
        # and L.data ->> 'skb1_saknr_key' = R.ska1_saknr_key
        # """
        #
        # j32= """
        # drop table if exists caps_14;
        # select L.*,
        # R.*
        # into caps_14
        # from caps_13 as L
        # left join J2_SKB1_SKA1_SKAT as R
        # on L.data ->> 'co_code_gl' = R.'skb1_bukrs_key'
        #"""

        #Join REGUP to T001
        j41 = """
        drop table if exists J1_REGUP_T001;
        select
        L.data ->> 'pymt_doc_num_pmt' as pymt_doc_num_pmt,
        L.data ->> 'regup_bukrs_key' as regup_bukrs_key,
        L.data ->> 'regup_buzei_key' as regup_buzei_key,
        L.data ->> 'regup_ebeln_key' as regup_ebeln_key,
        L.data ->> 'regup_ebelp_key' as regup_ebelp_key,
        L.data ->> 'payee_code_pmt' as payee_code_pmt,
        L.data ->> 'regup_gjahr_key' as regup_gjahr_key,
        L.data ->> 'regup_hkont_key' as regup_hkont_key,
        L.data ->> 'cx_num_pmt' as cx_num_pmt,
        L.data ->> 'regup_laufd_key' as regup_laufd_key,
        L.data ->> 'regup_laufi_key' as regup_laufi_key,
        L.data ->> 'regup_lifnr_key' as regup_lifnr_key,
        L.data ->> 'regup_saknr_key' as regup_saknr_key,
        L.data ->> 'regup_vblnr_key' as regup_vblnr_key,
        L.data ->> 'regup_xvorl_key' as regup_xvorl_key,
        L.data ->> 'co_code_pmt' as co_code_pmt,
        L.data ->> 'regup_zlsch_key' as regup_zlsch_key,
        R.data ->> 't001_bukrs_key' as t001_bukrs_key,
        R.data ->> 'co_name' as co_name,
        R.data ->> 't001_land1_key' as t001_land1_key
        into J1_REGUP_T001
        from (select * from sap_regup where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_t001 where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'co_code_pmt' = R.data ->> 't001_bukrs_key'
        """
        ##Join T042ZT to PAYR, However T042ZT is missing in data request
        # j42 = """
        # drop table if exists J1_T042ZT_PAYR;
        # select
        # L.data ->> 't042zt_land1_key' as t042zt_land1_key,
        # L.data ->> 't042zt_spras_key' as t042zt_spras_key,
        # L.data ->> 'pymt_method_pmt' as pymt_method_pmt,
        # L.data ->> 't042zt_zlsch_key' as t042zt_zlsch_key,
        # R.data ->> 'check_num_pmt' as check_num_pmt,
        # R.data ->> 'payr_hbkid_key' as payr_hbkid_key,
        # R.data ->> 'payr_rzawe_key' as payr_rzawe_key,
        # R.data ->> 'pymt_dt_pmt' as pymt_dt_pmt,
        # R.data ->> 'payr_zbukr_key' as payr_zbukr_key
        # into J1_T042ZT_PAYR
        # from (select  * from sap_t001 where capsgen_id = {capsgen_id}) as L
        # left join (select * from sap_t042zt where capsgen_id = {capsgen_id}) as R
        # on L.data ->> 't042zt_zlsch_key' = R.data ->> 'payr_rzawe_key'
        # """
        ##Join REGUP to T042ZT+PAYR, However T042ZT is missing in data request
        # j33 = """
        # drop table if exists J2_REGUP_T001_T042ZT_PAYR
        # select
        # L.*,
        # R.*
        # into J2_REGUP_T001_T042ZT_PAYR
        # from J1_REGUP_T001 as L
        # left join (select * from J1_T042ZT_PAYR) as R
        # on L.regup_zlsch_key = R.t042zt_zlsch_key
        # """
        #Join REGUP to KNA1 (However KNA1 is missing from CDM)
        # j34 = """
        # drop table if exists J3_REGUP_T001_T042ZT_PAYR_KNA1;
        # select L.*,
        # R.data ->> 'kna1_kunnr_key' as kna1_kunnr_key
        # into J3_REGUP_T001_T042ZT_PAYR_KNA1;
        # from J2_REGUP_T001_T042ZT_PAYR as L
        # left join (select * from sap_kna1 where capsgen_id = {capsgen_id}) as R
        # on L.cx_num_pmt = R.data ->> 'kna1_kunnr_key'
        # """
        #Join REGUP to LFA1
        j35 = """
        drop table if exists J2_REGUP_T001_LFA1;
        select L.*,
        R.data ->> 'lfa1_lifnr_key' as lfa1_lifnr_key
        into J2_REGUP_T001_LFA1
        from J1_REGUP_T001 as L
        left join (select * from sap_lfa1 where capsgen_id = {capsgen_id}) as R
        on L.regup_lifnr_key = R.data ->> 'lfa1_lifnr_key'
        """
        # #Join REGUP to ANLA, however ANLA is not present in CDM
        # j34 = """
        # drop table if exists J3_REGUP_T001_LFA1_ANLA;
        # select L.*,
        # R.data ->> 'anla_bukrs_key' as anla_bukrs_key,
        # R.data ->> 'anla_anln1_key' as anla_anln1_key,
        # R.data ->> 'anla.anln2_key' as anla.anln2_key
        # into J3_REGUP_T001_LFA1_ANLA
        # from J2_REGUP_T001_LFA1 as L
        # left join (select * from sap_anla where capsgen_id = {capsgen_id}) as R
        # on L.regup_bukrs_key = R.data ->> 'anla_bukrs_key'
        # and
        # L.regup_anln1_key = R.data ->> 'anla_anln1_key'
        # and
        # L.regup_anln2_key = R.data ->> 'anla_regup_key'
        # """
        #Join REGUP to EKPO
        j35 = """
        drop table if exists j3_regup_t001_lfa1_ekpo;
        select L.*,
        R.data ->> 'ekpo_ebeln_key' as ekpo_ebeln_key,
        R.data ->> 'ekpo_ebelp_key' as ekpo_ebeln_key
        into j3_regup_t001_lfa1_ekpo
        from J2_REGUP_T001_LFA1 as L
        left join (select * from sap_ekpo where capsgen_id = {capsgen_id}) as R
        on L.regup_ebeln_key = R.ekpo_ebeln_key
        and
        L.regup_ebelp_key = R.ekpo_ebelp_key
        """

        j36 = """
        drop table if exists J3_SKB1_REGUP_T001_LFA1_EKPO;
        select L.*,
        R.*
        into J3_SKB1_SKA1_SKAT_REGUP_T001_LFA1_EKPO
        from (select * from sap_skb1 where capsgen_id = {capsgen_id}) as L
        left join (select * from j3_regup_t001_lfa1_ekpo) as R
        on L.data ->> 'skb1_bukrs_key' = R.regup_bukrs_key
        and
        L.data ->> 'skb1_saknr_key' = R.regup_saknr_key
        """

        j37 = """
        drop table if exists caps_6
        select L.*,
        R.*
        into caps_6
        from caps_5 as L
        left join J3_SKB1_REGUP_T001_LFA1_EKPO as R
        on L.co_code_gl = R.skb1_bukrs_key
        and
        L.largest_debit_half_acct_num_gl = R.skb1_saknr_key
        """
        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return jsonify(response), 200

def caps_to_erd_2():
    try:
        # #Join TOA01, but missing join relationship
        # j11 = """
        # drop table if exists caps_7;
        # select L.*,
        # R.data ->> 'toa01_sap_object_key' as toa01_sap_object_key,
        # R.data ->> 'toa01_object_id_key' as toa01_object_id_key,
        # R.data ->> 'toa01_archiv_id_key' as toa01_archiv_id_key,
        # R.data ->> 'toa01_arc_doc_id_key' as toa01_arc_doc_id_key,
        # R.data ->> 'ar_object' as ar_object,
        # R.data ->> 'ar_date' as ar_date,
        # R.data ->> 'del_date' as del_date
        # into caps_7
        # from caps_6 as L
        # left join (select * from sap_toa01 where capsgen_id = {capsgen_id}) as R
        # on L.
        # """.format(capsgen_id = data['capsgen_id'])

        j2 = """
        drop table if exists J1_LFA1_LFM1;
        select
        L.data ->> 'lfa1_lifnr_key' as lfa1_lifnr_key,
        L.data ->> 'lfa1_land1_key' as lfa1_land1_key,
        L.data ->> 'vend_name' as vend_name,
        L.data ->> 'vend_city' as vend_city,
        L.data ->> 'vend_region' as vend_region,
        L.data ->> 'vend_tax_num_1' as vend_tax_num_1,
        L.data ->> 'vend_tax_num_2' as vend_tax_num_2,
        L.data ->> 'vend_tax_num_3' as vend_tax_num_3,
        L.data ->> 'vend_tax_num_4' as vend_tax_num_4,
        L.data ->> 'vend_tax_num_5' as vend_tax_num_5,
        L.data ->> 'vend_tax_num_type' as vend_tax_num_type,
        L.data ->> 'vend_reg_num' as vend_reg_num,
        R.data ->> 'lfm1_ekorg_key' as lfm1_ekorg_key,
        R.data ->> 'incoterms1' as incoterms1,
        R.data ->> 'incoterms2' as incoterms2,
        R.data ->> 'lfm1_lifnr_key' as lfm1_lifnr_key
        into J1_LFA1_LFM1
        from (select * from sap_lfa1 where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_lfm1 where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'lfa1_land1_key' = R.data ->> 'lfm1_lifnr_key'
        """

        j3 = """
        drop table if exists J2_LFA1_LFM1_LFAS;
        select
        L.*,
        R.data ->> 'lfas_lifnr_key' as lfas_lifnr_key,
        R.data ->> 'lfas_land1_key' as lfas_land1_key,
        R.data ->> 'stceg' as lfas_stceg_key
        into J2_LFA1_LFM1_LFAS
        from j1_lfa1_lfm1 as L
        left join (select * from sap_lfas where capsgen_id = {capsgen_id}) as R
        on L.lfa1_lifnr_key = R.data ->> 'lfas_lifnr_key'
        """

        j4 = """
        drop table if exists j3_lfa1_lfm1_lfas_t005t;
        select
        L.*,
        R.data ->> 't005t_land1_key' as t005t_land1_key,
        R.data ->> 'cntry_name' as cntry_name,
        R.data ->> 't005t_spras_key' as t005t_spras_key
        into j3_lfa_lfm1_lfas_t005t
        from j2_lfa1_lfm1_lfas as L
        left join (select * from sap_t005t where capsgen_id = {capsgen_id}) as R
        on L.lfa1_land1_key = R.data ->> 't005t_land1_key'
        """

        # #Join LFA1 to J_1ATODCT, but this is missing from data request.
        # j5 = """
        # drop table if exists j4_lfa1_lfm1_lfas_t005t_j_1atodct;
        # select
        # L.*,
        # R.data ->> 'j_1atodct_j_1atodct_key' as j_1atodct_j_1atodct_key,
        # R.data ->> 'j_1atodct_spras_key' as j_1atodct_spras_key,
        # R.data ->> 'tx_type_descr_tx' as tx_type_descr_tx
        # into j4_lfa1_lfm1_lfas_t005t_j_1atodct
        # from j3_lfa_lfm1_lfas_t005t as L
        # left join (select * from sap_j_1atodct where capsgen_id = {capsgen_id}) as R
        # on L.vend_tax_num_type = R.data ->> 'j_1atodct_j_1atodct_key'
        # """

        #Join LFA1 to BSAK
        j6 = """
        drop table if exists j4_lfa1_lfm1_lfas_t005t_bsak;
        select
        L.*,
        R.data ->> 'bsak_augbl_key' as bsak_augbl_key,
        R.data ->> 'bsak_augdt_key as bsak_augdt_key,
        R.data ->> 'bsak_belnr_key as bsak_belnr_key,
        R.data ->> 'bsak_bukrs_key as bsak_bukrs_key,
        R.data ->> 'bsak_buzei_key as bsak_buzei_key,
        R.data ->> 'bsak_gjahr_key as bsak_gjahr_key,
        R.data ->> 'bsak_lifnr_key as bsak_lifnr_key,
        R.data ->> 'spec_trnx_type_gl as spec_trnx_type_gl,
        R.data ->> 'spec_indicator_gl as spec_indicator_gl,
        R.data ->> 'cash_disc_percent_1_gl as cash_disc_percent_1_gl,
        R.data ->> 'cash_disc_days_1_gl as cash_disc_days_1_gl,
        R.data ->> 'cash_disc_percent_2_gl as cash_disc_percent_2_gl,
        R.data ->> 'cash_disc_days_2_gl as cash_disc_days_2_gl,
        R.data ->> 'pymt_period_gl as pymt_period_gl,
        R.data ->> 'pymt_terms_gl as pymt_terms_gl,
        R.data ->> 'assign_num_gl as assign_num_gl
        into j4_lfa1_lfm1_lfas_t005t_bsak
        from j3_lfa_lfm1_lfas_t005t as L
        left join (select * from sap_bsak where capsgen_id = {capsgen_id}) as R
        on L.lfa1_lifnr_key = R.bsak_lifnr_key
        """
        #Join LFA1+LFM1+LFAS+T005T+bsak on CAPS
        j7 = """
        drop table if exists caps_7;
        select
        L.*,
        R.*
        into caps_7
        from caps_6 as L
        left join (select * from j4_lfa1_lfm1_lfas_t005t_bsak) as R
        on L.vend_num = R.lfa1_lifnr_key
        """

        j8 = """
        drop table if exists j1_MARA_TSKMT;
        select
        L.data ->> 'ean_upc_num_mat' as ean_upc_num_mat,
        L.data ->> 'mara_gewei_key' as mara_gewei_key,
        L.data ->> 'mat_orig_ctry_mat' as mat_orig_ctry_mat,
        L.data ->> 'mara_magrv_key' as mara_magrv_key,
        L.data ->> 'mara_matkl_key' as mara_matkl_key,
        L.data ->> 'mara_matnr_key' as mara_matnr_key,
        L.data ->> 'mara_mfrnr_key' as mara_mfrnr_key,
        L.data ->> 'ean_categ_mat' as ean_categ_mat,
        L.data ->> 'mat_tx_class_mat' as mat_tx_class_mat,
        L.data ->> 'mara_voleh_key' as mara_voleh_key,
        L.data ->> 'ergei' as ergei,

        R.data ->> 'tskmt_spras_key' as tskmt_spras_key,
        R.data ->> 'tskmt_tatyp_key' as tskmt_tatyp_key,
        R.data ->> 'tskmt_taxkm_key' as tskmt_taxkm_key,
        R.data ->> 'mat_tx_class_descr_mat' as mat_tx_class_descr_mat
        into j1_MARA_TSKMT
        from (select * from sap_mara where capsgen_id = {capsgen_id}) as L
        left join (select * from tskmt where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'mara_taxkm_key' = R.data ->> 'tskmt_taxkm_key'
        ;
        """

        j9 = """
        drop table if exists J2_MARA_TSKMT_T023T;
        select
        L.*,
        R.data ->> 't023t_matkl_key' as t023t_matkl_key,
        R.data ->> 't023t_spras_key' as t023t_spras_key,
        R.data ->> 'mat_group_descr_mat' as mat_group_descr_mat
        into J2_MARA_TSKMT_T023T
        from J1_MARA_TSKMT as L
        left join (select * from sap_t023t where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'mara_matkl_key' = R.data ->> 't023t_matkl_key';
        """

        j10 = """
        drop table if exists j1_MARA_TSKMT;
        select
        L.data ->> 'ean_upc_num_mat' as ean_upc_num_mat,
        L.data ->> 'mara_gewei_key' as mara_gewei_key,
        L.data ->> 'mat_orig_ctry_mat' as mat_orig_ctry_mat,
        L.data ->> 'mara_magrv_key' as mara_magrv_key,
        L.data ->> 'mara_matkl_key' as mara_matkl_key,
        L.data ->> 'mara_matnr_key' as mara_matnr_key,
        L.data ->> 'mara_mfrnr_key' as mara_mfrnr_key,
        L.data ->> 'ean_categ_mat' as ean_categ_mat,
        L.data ->> 'mat_tx_class_mat' as mat_tx_class_mat,
        L.data ->> 'mara_voleh_key' as mara_voleh_key,
        R.data ->> 'tskmt_spras_key' as tskmt_spras_key,
        R.data ->> 'tskmt_tatyp_key' as tskmt_tatyp_key,
        R.data ->> 'tskmt_taxkm_key' as tskmt_taxkm_key,
        R.data ->> 'mat_tx_class_descr_mat' as mat_tx_class_descr_mat
        into j1_MARA_TSKMT
        from (select * from sap_mara where capsgen_id = {capsgen_id}) as L
        left join (select * from tskmt where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'mara_taxkm_key' = R.data ->> 'tskmt_taxkm_key'
        ;
        """
        j11 = """
        drop table if exists J2_MARA_TSKMT_T023T;
        select
        L.*,
        R.data ->> 't023t_matkl_key' as t023t_matkl_key,
        R.data ->> 't023t_spras_key' as t023t_spras_key,
        R.data ->> 'mat_group_descr_mat' as mat_group_descr_mat
        into J2_MARA_TSKMT_T023T
        from J1_MARA_TSKMT as L
        left join (select * from sap_t023t where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'mara_matkl_key' = R.data ->> 't023t_matkl_key';
        """

        j12 = """
        drop table if exists J3_MARA_TSKMT_T023T_T006A;
        select
        L.*,
        R.data ->> 't006a_spras_key' as t006a_spras_key,
        R.data ->> 't006a_msehi_key' as t006a_msehi_key,
        R.data ->> 'mseh3' as mseh3
        into J3_MARA_TSKMT_T023T_T006A
        from J2_MARA_TSKMT_T023T as L
        left join (select * from sap_t006a where capsgen_id = {capsgen_id}) as R
        on CONCAT(L.ergei, L.mara_gewei_key,  L.mara_voleh_key) = R.data ->> 't006a_msehi_key';
        """

        j13 = """
        drop table if exists J4_MARA_TSKMT_T023T_T006A_MAKT;
        select
        L.*,
        R.data ->> 'mat_descr_mat'as mat_descr_mat,
        R.data ->> 'makt_matnr_key' as makt_matnr_key,
        into J4_MARA_TSKMT_T023T_T006A_MAKT
        from J3_MARA_TSKMT_T023T_T006A as L
        left join (select * from sap_makt where capsgen_id = {capsgen_id}) as R
        on L.mara_matnr_key = R.data ->> 'makt_matnr_key'
        """

        j14 = """
        drop table if exists J1_MLAN_T005T;
        select
        L.data ->> 'mat_dept_ctry_mat' as mat_dept_ctry_mat,
        L.data ->> 'mlan_matnr_key' as mlan_matnr_key,
        L.data ->> 'mat_tx_ind_mat' as mat_tx_ind_mat,
        L.data ->> 'TAXM1' as TAXM1,
        L.data ->> 'TAXm2' as TAXM2,
        R.t005t_land1_key,
        R.cntry_name,
        R.t005t_spras_key
        into J1_MLAN_T005T
        from (select * from sap_t005t where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_mlan where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'mat_dept_ctry_mat' = R.data ->> 't005t_land1_key'
        """

        j15 = """
        drop table if exists J5_MARA_TSKMT_T023T_T006A_MAKT_MLAN_T005T;
        select
        L.*,
        R.*
        into J5_MARA_TSKMT_T023T_T006A_MAKT_MLAN_T005T
        from J4_MARA_TSKMT_T023T_T006A_MAKT as L
        left join J1_MLAN_T005T as R
        on L.mara_matnr_key = R.mlan_matnr_key;
        """

        j16 = """
        drop table if exists caps_8;
        select
        L.*,
        R.*
        into caps_8
        from caps_7 as L
        left join J5_MARA_TSKMT_T023T_T006A_MAKT_MLAN_T005T as R
        on L.data ->> 'material_num_gl' = R.mara_matnr_key
        """




        j16 = """
        drop table if exists J1_MSEG_T001W;
        select
        L.data ->> 'mat_doc_num_mat' as mat_doc_num_mat,
        L.data ->> 'mseg_mjahr_key' as mseg_mjahr_key,
        L.data ->> 'mseg_zeile_key' as mseg_zeile_key,
        L.data ->> 'mat_plnt_mat' as mat_plnt_mat,
        L.data ->> 'mseg_ebeln_key' as mseg_ebeln_key,
        L.data ->> 'mseg_ebelp_key' as mseg_ebelp_key,
        L.data ->> 'matnr' as matnr,
        L.data ->> 'umwrk' as umwrk,
        R.data ->> 'plant_name_plant' as plant_name_plant,
        R.data ->> 'plant_tx_jur_plant' as plant_tx_jur_plant,
        R.data ->> 't001w_werks_key' as t001w_werks_key
        into j1_MSEG_T001W
        from (select * from sap_mseg where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_t001w where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'mat_plnt_mat' = R.data ->> 't001w_werks_key';
        """

        #Join MARA to EKPO

        #Join EKKO to T024E
        j17 = """
        drop table if exists J1_EKKO_T024E;
        select
        L.data ->> 'ekko_ebeln_key' as ekko_ebeln_key,
        L.data ->> 'punch_grp_po' as punch_grp_po,
        L.data ->> 'punch_org_po' as punch_org_po,
        L.data ->> 'handover_loc_po',
        L.data ->> 'vend_phone',
        L.data ->> 'vend_person',
        L.data ->> 'STCEG' as STCEG,
        R.data ->> 't024e_ekorg_key',
        R.data ->> 'purch_org_descr_po'
        into j1_EKKO_T024E
        from (select * from sap_ekko where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_t024e where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'ekko_ebeln_key' = R.data ->> 't024e_ekorg_key'
        """

        j18 = """
        drop table if exists J1_EKPO_T001L;
        select
        L.data ->> 'wbs_po' as wbs_po,
        L.data ->> 'ekpo_ebeln_key' as ekpo_ebeln_key,
        L.data ->> 'ekpo_ebelp_key' as ekpo_ebelp_key,
        L.data ->> 'ekpo_ematn_key' as ekpo_ematn_key,
        L.data ->> 'ekpo_lgort_key' as ekpo_lgort_key,
        L.data ->> 'po_tx_code_po' as po_tx_code_po,
        L.data ->> 'plant_num' as plant_num,
        L.data ->> 'po_tx_jur' as po_tx_jur,
        L.data ->> 'po_item_descr' as po_item_descr
        R.data ->> 'stor_loc_desc_mat' as stor_loc_desc_mat,
        R.data ->> 'stor_loc_mat' as stor_loc_mat,
        R.data ->> 'stor_plant_mat' as stor_plant_mat
        into J1_EKPO_T001L
        from (select * from sap_ekpo) where capsgen_id = {capsgen_id}) as L
        left join (select * from sap_t001l where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'plant_num' = R.data ->> 'stor_plant_mat'
        and
        L.data ->> 'ekpo_lgort_key' = R.data ->> 'stor_loc_mat'
        """

        #Issues where EKPO does not have reswk column
        # j19 = """
        # drop table if exists J2_EKPO_T001L_T001W;
        # select
        # L.*,
        # R.data ->> 't001w_werks_key' as t001w_werks_key,
        # R.data ->> 'plant_tx_jur_plant' as plant_tx_jur_plant,
        # R.data ->> 'plant_name_plant' as plant_name_plant
        # into J2_EKPO_T001L_T001W
        # from J1_EKPO_T001L as L
        # left join (select * from sap_T001w where capsgen_id = {capsgen_id}) as R
        # on L.data ->> '' = R.data ->> 't001w_werks_key'

        j20 = """
        drop table if exists J2_EKPO_T001L_TTXJT;
        select
        L.*,
        R.data ->> 'ttxjt_kalsm_key' as ttxjt_kalsm_key,
        R.data ->> 'ttxjt_spras_key' as ttxjt_spras_key,
        R.data ->> 'tx_jur_descr_tx' as tx_jur_descr_tx,
        R.data ->> 'ttxjt_txjcd_key' as ttxjt_txjcd_key
        into J2_EKPO_T001L_TTXJT
        from J1_EKPO_T001L as L
        left join (select * from sap_t001l where capsgen_id = {capsgen_id}) as R
        on L.po_tx_jur = R.data ->> 'ttxjt_txjcd_key'
        """

        j21 = """
        drop table if exists J3_EKPO_T001L_TTXJT_MSEG_T001W;
        select
        L.*,
        R.*
        into J3_EKPO_T001L_TTXJT_MSEG_T001W
        from J2_EKPO_T001L_TTXJT as L
        left join J1_MSEG_T001W as R
        on L.data ->> 'ekpo_ebeln_key' = R.data ->> 'mseg_ebeln_key'
        AND
        L.ekpo_ebelp_key = R.mseg_ebelp_key
        """
        j21 = """
        drop table if exists J3_EKPO_T001L_TTXJT_MSEG_T001W_EKKO_T024E;
        select
        L.*,
        R.*
        into J3_EKPO_T001L_TTXJT_MSEG_T001W_EKKO_T024E
        from J2_EKPO_T001L_TTXJT as L
        left join J1_EKKO_T024E as R
        on L.ekpo_ebeln_key = R.ekko_ebeln_key
        """

        j22 = """
        drop table if exists caps_9;
        select
        L.*,
        R.*
        into caps_9
        from caps_8 as L
        left join j4_lfa1_lfm1_lfas_t005t_bsak as R
        on L.data ->> 'vend_num' = R.lfa1_lifnr_key
        """





























        response['message'] = ''
        response['payload'] = []
    except Exception as e:
        response['status'] = 'error'
        response['message'] = str(e)
    return jsonify(response), 200
@sap_caps_gen.route('caps_calculations', methods=['POST'])
def caps_erd_calculations():
    try:
        j99 = """
        ## WARNING: Not every client uses these document types consistently.
        DROP TABLE IF EXISTS RAW;
        select *
        into RAW
        from J10_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT_T007
        where ltrim(rtrim(BLART)) in ('AN', 'FD', 'FP', 'FY', 'RE', 'RX', 'SA', 'GG', 'GP', 'VC', 'VT')
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
