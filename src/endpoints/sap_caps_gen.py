'''
sap_caps_gen endpoints
'''
import csv
import decimal
import datetime
import json
import logging
import glob
import os
import itertools
import pandas as pd
import random
import re
import shutil
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


@sap_caps_gen.route('/unzipping', methods=['POST'])
def unzipping():
    """
    This is a function that iterates through each folder in the directory, and recursively walks to the nth level of the folder, retrieving any zipped files.
    Example Payload: {"client" : "Repsol" ,"project": "Repsol-2019", "system" : "SAP", "file" : "sanic.png", "debug" : True}
    """

    def extract_nested_zip(zippedFile, toFolder):
        try:
            with zipfile.ZipFile(zippedFile, 'r') as zfile:
                zfile.extractall(path=toFolder)
        except NotImplementedError:
            response['status'] = 'Incorrect compression type. Please extract manually and store into staged_for_db folder.'
            return 'Incorrect compression type. Please extract manually and store into staged_for_db folder.'
        except Exception as e:
            response['status'] = 'There were errors unzipping one of the zipped files inside. Please check error log.'
            response['message'] = response['message'] + ('Failed on ' + str(zippedFile) + ' ')
            os.remove(zippedFile)
            print(zippedFile + 'has been removed')
            return (zippedFile +  'failed to unzip!')
        os.remove(zippedFile)
        print(zippedFile + 'has been removed')
        for root, dirs, files in os.walk(toFolder):
            for filename in files:
                #print(len(filename))
                if re.search(r'\.(?i)ZIP$', filename):
                    fileSpec = os.path.join(root, filename)
                    print(fileSpec)
                    try:
                        extract_nested_zip(fileSpec, root)
                    except Exception as e:
                        pass
    response = {'status': '', 'message': '', 'payload': []}
    data = request.get_json()
    if data is not None and data['debug'] == False:
        print('debug set to False')
    if os.listdir('caps_gen_processing/caps_gen_raw') is not None:
        #try:
        #logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)
        current_input_path = get_cwd('caps_gen_processing/caps_gen_raw')
        print(current_input_path)
        current_output_path = get_cwd('caps_gen_processing/caps_gen_unzipped')
        cwd = os.getcwd()
        os.chdir(current_input_path)
        extension = '.zip'
        for item in os.listdir(current_input_path):
            if item.lower().endswith(extension):
                try:
                    print(item)
                    extract_nested_zip(item, current_output_path)
                except Exception as e:
                    response['status'] = 'Cannot unzip input zip'
                    response['message'] = response['message'] + ('Failed on ' + str(item))
        os.chdir(cwd)
        #except Exception as e:
            #response['message'] = 'Successfully downloaded, but unable to access caps_gen_unzipped folder'
            #return 'Unable to access folder.'
    print('Data Received: "{data}"'.format(data=data))
    return response

#MAPPING HAPPENS

def completeness_check(column):
    completeness_response = {}
    for index, elem in enumerate(column):
        if '' == elem or elem.isspace():
            completeness_response[str(index)] = elem
    completeness_response['final_score'] = 100 - (len(completeness_response)/len(column))
    return completeness_response

def validity_check(column_data, regex):
    validity_response = {}
    results = list(filter(re.compile(regex).match, column_data))
    validity_response['results'] = results
    validity_response['final_score'] = 100 - (len(validity_response['results'])/len(column_data))
    return validity_response

@sap_caps_gen.route('/build_master_tables', methods=['GET'])
def build_master_tables():
    def linking_fields_serializer(label):
        return {
            "table_name": label.table_name,
            "field_name": label.field_name,
            "is_complete": label.is_complete,
            "is_unique": label.is_unique,
            "regex": label.regex
        }

    list_tablenames = ['AUFK', 'BSAK', 'BSEG', 'BKPF', 'CEPCT', 'CSKS', 'CSKT', 'EKKO', 'EKPO', 'IFLOT', 'ILOA', 'LFA1' ,'MAKT', 'MARA', 'PAYR', 'PROJ' ,'PRPS', 'SKAT', \
    'T001', 'T001W', 'T007', 'T007S']
    list_tablenames = ['LFA1']
    response = {'status': '', 'message': {}, 'payload': []}
    for table in list_tablenames:
        table_results = {}
        print(table)
        list_of_files = []
        for file in os.listdir(get_cwd('caps_gen_processing/caps_gen_unzipped')):
            if re.search(table, file):
                if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
                    list_of_files.append(file)
        wfd = open(get_cwd(os.path.join('caps_gen_processing/caps_gen_master', '{}_MASTER.txt'.format(table))), 'wb')
        for index, file in enumerate(list_of_files):
            # for first file
            if index == 0:
                with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_unzipped', file)), 'r' ,encoding='utf-8-sig') as fd:
                    #   get first line
                    #   change headers on first line to desired values
                    first_line = fd.readline()
                    table_results['header'] = first_line
                    first_line = first_line.encode()
                    #   add header to wfd
                    wfd.write(first_line)
                #   add rest of file to wfd
                    wfd.write(fd.read().encode())
            else:
                # for all future files
                with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_unzipped', file)), 'r', encoding='utf-8-sig') as fd:
                    #   strip header
                    next(fd)
                    wfd.write(fd.read().encode())
        wfd.close()
        print('table renamed to')
        referenceclass = eval('Sap' + str(table.lower().capitalize()))
        print(referenceclass)
        exampledump = []
        counter = 0
        with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_master', '{}_MASTER.txt'.format(table))), 'r', encoding='utf-8-sig') as masterfile:
            #masterfile = [next(masterfile) for x in range(10000)]
            for line in csv.DictReader((line.replace('#|#', 'ø') for line in masterfile), delimiter='ø', quoting=csv.QUOTE_NONE):
                counter += 1
                print(counter)
                dict_to_insert = {'data' : line}
                dict_to_insert['project_id'] = 1
                exampledump.append(dict_to_insert)
        db.session.bulk_insert_mappings(referenceclass, exampledump)
        db.session.commit()
        print('great success')
    return 'OK'

######################### MAPPING HAPPENS HERE #######################################

@sap_caps_gen.route('/rename_scheme', methods=['GET'])
def rename_scheme():
    def rename_query_serializer(row):
        return {
            "id": row.id,
            "data": row.data
        }

    def rename_builder(table):
        rename_dict = {}
        for index, elem in enumerate(mapping):
            if mapping[index]['mappings'][0]['table_name'] == table:
                rename_dict.update({mapping[index]['mappings'][0]['column_name']: mapping[index]['script_label']})
        return rename_dict

    mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
    list_tablenames = list(set([table['mappings'][0]['table_name'] for table in mapping]))
    list_tablenames = ['BSEG', 'BKPF']

    for table in list_tablenames:
        renamed_columndata = []
        print(table)
        renaming_scheme = rename_builder(table)
        tableclass = eval('Sap' + str(table.lower().capitalize()))
        columndata = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).all()
        #columndata = list(list(zip(*tableclass.query.with_entities(getattr(tableclass, 'data')).all()))[0])
        #print(renaming_scheme)
        import time

        start_time = time.time()
        for row in columndata:
            try:
                row = rename_query_serializer(row)
                for key, value in renaming_scheme.items():
                    row['data'][value] = row['data'].pop(key)
            except KeyError as e:
                print('missing CDM label column' + str(e))

            renamed_columndata.append(row)
        print("--- %s seconds ---" % (time.time() - start_time))
        db.session.bulk_update_mappings(tableclass, renamed_columndata)
        db.session.commit()
        print('great success')
    return 'OK'

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
    def get_count(q):
        return q.query.with_entities(func.count()).scalar()


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
    list_tablenames = ['BKPF']
    for table in list_tablenames:
        data_dictionary_results[table] = {}
        print(table)
        tableclass = eval('Sap' + str(table.lower().capitalize()))

        print(tableclass)
        compiled_data_dictionary = data_dictionary(CDM_query, table)
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
        if len(dups) > 1:
            uniqueness_response = {}
            uniqueness_response['results'] = dups
            uniqueness_response['final_score'] = 100 - (len(dups)/tableclass.query.count())
            data_dictionary_results[table] = {'uniqueness' : uniqueness_response}
        import json
        for column in compiled_data_dictionary.keys():
            completeness_response = {}
            print(column)
            column = 'company_code'
            query = tableclass.query
            query = query.with_entities(getattr(tableclass, 'data')).limit(2).all()
            query = [regex_serializer(row)['data'][column] for row in query]
            if compiled_data_dictionary[column]['regex']:
                data_dictionary_results[table][column] = {
                    'regex': validity_check(query, compiled_data_dictionary[column]['regex'])}
    return data_dictionary_results


@sap_caps_gen.route('/j1_j10', methods=['GET'])
def j1_j10():

    def execute(query):
        result = db.session.execute(query)
        db.session.commit()
        return 'query execute successful'


    j1 = """DROP TABLE IF EXISTS JOIN_BKPF_T001_MSTR;
    select
    L.*,
    R.data -> 'KTOPL' as KTOPL,
    ltrim(rtrim(cast(L.data ->> 'BUKRS' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'BELNR' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'GJAHR' AS Text))) varapkey
    into table JOIN_BKPF_T001_MSTR
    from
    (select * from sap_bkpf limit 100) as L
    inner join
    (select * from sap_t001 where CAST(data ->> 'SPRAS' AS TEXT) = 'EN') as R
    on CAST(L.data -> 'BUKRS' AS TEXT) = cast(R.data -> 'BUKRS' AS TEXT)"""


    j2 = """DROP TABLE IF EXISTS BSEG_AP;
    select
    L.*,
    ltrim(rtrim(cast(L.data ->> 'BUKRS' as Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'BELNR' AS Text))) || '_' || LTRIM(RTRIM(CAST(L.data ->> 'GJAHR' AS Text))) varAPKey,
    cast('' as text) AS varMultiVND,
    cast('' as text) as varSupplier_No
    into  BSEG_AP
    from (select * from sap_bseg) as L"""

    j3 = """DROP TABLE IF EXISTS distinctVarAPKeyVendorAcctNum;
    SELECT DISTINCT L.varAPKey, LTRIM(RTRIM(L.data ->> 'LIFNR')) AS LIFNR, Row_Number() Over(Partition by varAPKey ORDER BY L.data ->> 'LIFNR') AS RowNum
    INTO table distinctVarAPKeyVendorAcctNum
    FROM BSEG_AP AS L
    WHERE L.data ->> 'LIFNR' IS NOT NULL
                   AND LTRIM(RTRIM(L.data ->> 'LIFNR')) != ''"""

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
where R2.varMultiVND = 'Multi_Vendor'
"""



    j6 = """
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
    FROM BSEG_AP AS L
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


    j14 = """
    DROP TABLE IF EXISTS J9_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT;

SELECT L.*, R.data ->> 'KTEXT'
INTO J9_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT
FROM J8_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR AS L
LEFT JOIN (SELECT * FROM sap_cskt WHERE cast( data ->> 'SPRAS' as text) = 'EN') AS R
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

    j16 = """
    DROP TABLE IF EXISTS RAW;
select *
into RAW
from J10_BSEG_BKPF_LFA1_SKAT_OnlyAP_EKPO_MAKT_REGUP_REGUH_PAYR_CSKT_T007
where ltrim(rtrim(BLART)) in ('AN', 'FD', 'FP', 'FY', 'RE', 'RX', 'SA', 'GG', 'GP', 'VC', 'VT')
    """


@sap_caps_gen.route('/aps_quality_check', methods=['GET'])
def aps_quality_check():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)


@sap_caps_gen.route('/APS_to_CAPS', methods=['GET'])
def aps_quality_check():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)
