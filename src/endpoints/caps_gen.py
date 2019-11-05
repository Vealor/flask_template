'''
CapsGen endpoints
'''
import csv
import datetime
import json
import os
import re
import zipfile
import requests
import itertools
from collections import Counter
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from os import path
from src.models import *
from config import *
from sqlalchemy import exists, desc, create_engine
from sqlalchemy.inspection import inspect
from src.util import *
from src.errors import *
from src.wrappers import has_permission, exception_wrapper

caps_gen = Blueprint('caps_gen', __name__)
#===============================================================================
# GET ALL CAPS GEN
@caps_gen.route('/', defaults={'id':None}, methods=['GET'])
@caps_gen.route('/<int:id>', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_caps_gens(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query
    # ID filter
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise ValueError('ID {} does not exist.'.format(id))
    # Set ORDER
    query = query.order_by('created')
    # Set LIMIT
    query = query.filter_by(project_id = args['project_id']) if 'project_id' in args.keys() and args['project_id'].isdigit() else query
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(10000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['message'] = ''
    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# DELETE A CAPS GEN
@caps_gen.route('/<int:id>', methods=['DELETE'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def delete_caps_gens(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = CapsGen.query.filter_by(id=id).first()
    if not query:
        raise ValueError('CapsGen ID {} does not exist.'.format(id))

    # TODO: make sure user deleting capsgen is the user that made it!
    caps_gen = query.serialize
    db.session.delete(query)
    db.session.commit()
    response['message'] = 'Deleted caps_gen id {}.'.format(caps_gen['id'])
    response['payload'] = [caps_gen]
    return jsonify(response), 200


#===============================================================================
#===============================================================================
#===============================================================================
# Data Source Page
# upload data when pressing `Next`
@caps_gen.route('/init', methods=['POST'])
@jwt_required
# @has_permission([])
@exception_wrapper()
def init_caps_gen():
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()
    request_types = {
        'project_id': 'int',
        'file_name': 'str',
        'system': 'str'
    }
    validate_request_data(data, request_types)


    ### DEV => do local directory creation if required
    # if not os.path.exists(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']))):
    #     print('path does not exist, creating project')
    #     os.mkdir(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id'])))
    #     folders = ['sap_data', 'caps_gen_unzipped', 'caps_gen_raw', 'caps_gen_master']
    #     for folder in folders:
    #         os.mkdir((os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), folder)))
    # else:
    #     raise Exception('Path has already been created for project')
    ### Hopefully raises "ERROR UPLOADING DATA"


    ### DEV/PROD => data unzipping
    # try:
    #     source_data_unzipper(data, response) # pass filename here?
    # except Exception as e:
    #     current_output_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
    #     list(map(os.unlink, (os.path.join(current_output_path, f) for f in os.listdir(current_output_path))))
    #     raise Exception(e)
    ###

    ### DEV/PROD => Create CapsGen entitiy in DB
    # do before unzipping and store path in CapsGen?
    # will fail without login!



    # TODO: change for project specific is_completed
    in_progress = CapsGen.query.filter_by(is_completed=False).first()
    if in_progress:
        raise ValueError('Capsgen already in progress by user \'{}\' for project \'{}\''.format(in_progress.caps_gen_user.username if in_progress.caps_gen_user else 'None',in_progress.caps_gen_project.name))
    capsgen = CapsGen(
        user_id=current_user.id,
        project_id=data['project_id']
    )
    db.session.add(capsgen)
    db.session.flush()

    labels = [i.script_label for i in CDMLabel.query.all()]
    for label in labels:
        new_mapping = DataMapping(
            caps_gen_id = capsgen.id,
            cdm_label_script_label = label
        )
        db.session.add(new_mapping)
    db.session.commit()

    try:


        ### DEV/PROD => make master tables
        # list_tablenames = current_app.config['CDM_TABLES']
        # engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
        # #todo: add table to payload so cio can know which tables to view
        # for table in list_tablenames:
        #     table_files = []
        #     #Search for all files that match table
        #     for file in os.listdir(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])):
        #         if re.search(table, file):
        #             if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
        #                 table_files.append(file)
        #     #Load & union files into one master table in memory
        #     wfd = open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_MASTER_LOCATION'], '{}_MASTER.txt'.format(table)), 'wb')
        #     for index, file in enumerate(table_files):
        #         if index == 0:
        #             with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'], file), 'r' ,encoding='utf-8-sig') as fd:
        #                 wfd.write(fd.read().encode())
        #         else:
        #             # for all future files
        #             with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'], file), 'r', encoding='utf-8-sig') as fd:
        #                 #   strip header
        #                 next(fd)
        #                 wfd.write(fd.read().encode())
        #     wfd.close()
        #
        #     #initialize variables for bulk insertion
        #     referenceclass = eval('Sap' + str(table.lower().capitalize()))
        #     list_to_insert = []
        #     counter = 0
        #     #bulk insert into database
        #     with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), 'caps_gen_master', '{}_MASTER.txt'.format(table)), 'r', encoding='utf-8-sig') as masterfile:
        #         header = masterfile.readline()
        #         header = header.rstrip('\n').split('#|#')
        #         for line in masterfile:
        #             # insert rows chunk by chunk to avoid crashing
        #             #  NOTE: 20,000 entries use about 4GB ram
        #             if counter >= 200000:
        #                 engine.execute(referenceclass.__table__.insert(), list_to_insert)
        #                 counter = 0
        #                 list_to_insert = []
        #             else:
        #                 counter += 1
        #                 list_to_insert.append({"capsgen_id": capsgen.id, 'data': dict(zip(header, line.rstrip('\n').split('#|#')))})
        #         if counter > 0:
        #             engine.execute(referenceclass.__table__.insert(), list_to_insert)
        #
        #     CapsGen.query.filter(CapsGen.project_id == data['project_id']).update({"is_completed": True})
        #     db.session.flush()
        ###

        # get data from blob and put into capsgen tables

        db.session.commit()
        response['message'] = 'Data successfully uploaded and CapsGen initialized.'
        response['payload'] = [CapsGen.find_by_id(capsgen.id).serialize]
    except Exception as e:
        # delete created caps_gen
        db.session.delete(capsgen)
        db.session.commit()
        raise Exception(e)

    return jsonify(response), 200

#===============================================================================
# Master Table headers  `table_name::column_name` list
# get master table data from caps_gen tables
@caps_gen.route('/<int:id>/master_table_headers', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def get_master_table_headers(id):
    def get_column_name(table, caps_data):
        return [{'table_name': table, 'column_name': header } for header in list(caps_data['data'].keys())]
    
    # def filter_column_name(mappings, table_headers):
    #     print("yeyeeyey")
    #     for 
    #     if table_headers.key() in mappings.keys():
    #         for column_name in table_headers.values():
    #             if column_name['column_name'] in mappings[table_headers.key()]:
    #                 table_headers.
    #     return True


    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    mappings = {}
    for i in DataMapping.query.filter_by(caps_gen_id=id).all():
        if i.serialize['table_column_name']:
            table_column_name = i.serialize['table_column_name']
            table_name = table_column_name[0]['table_name'].lower()
            if table_name in mappings.keys():
                mappings[table_name] = mappings[table_name] + [table_column_name[0]['column_name'].lower()]
            else:
                mappings[table_name] = [table_column_name[0]['column_name'].lower()]
      
    # get all data from all tables for given capsgen
    headers = [{table.partition('sap')[2].lower(): list(itertools.chain.from_iterable(list(map(lambda x: get_column_name(table.partition('sap')[2].lower(), x), value))))} for table, value in query.first().serialize['caps_data'].items()]
    # get rid of the mapped headers
    for table_header in headers:
        for table_name in table_header.keys():
            if table_name in mappings.keys():
                for column_name in table_header[table_name]:
                    if column_name in mappings[table_name]:
                        column_names.remove(column_name)

    response['playload'] = headers
    # response['payload'] = [list(itertools.chain.from_iterable(list(map(get_column_name, value)))) for table, value in query.first().serialize['caps_data'].items()]
    return jsonify(response), 200

#===============================================================================

#>>> DO MAPPING with mapping endpoints

#===============================================================================
# Apply Mappings Button
# upload data when pressing `Apply` and build gst registration for caps gen
# renames columns as per mapping. Do not run this yet if you plan to execute J1
# to J10; as the joins are currently hardcoded to their original names.
# the top priority is to complete caps; and CDM is not final yet so CDM labels
# will not be written in.
@caps_gen.route('/<int:id>/apply_mappings_build_gst_registration', methods=['POST'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def apply_mappings_build_gst_registration(id):
    response = {'status': 'ok', 'message': {}, 'payload': []}
    response.update({'renaming': {'status': 'ok', 'message': '', 'payload': []}})
    data = request.get_json()

    mapping = [label.serialize for label in CDMLabel.query.all()]
    list_tablenames = current_app.config['CDM_TABLES']
    for table in list_tablenames:
        renamed_columndata = []
        rename_scheme = {}
        errorlines = []
        for index, elem in enumerate(mapping):
            if mapping[index]['mappings'][0]['table_name'] == table:
                rename_scheme.update({mapping[index]['mappings'][0]['column_name']: mapping[index]['script_label']})
        tableclass = eval('Sap' + str(table.lower().capitalize()))
        columndata = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).filter(tableclass.capsgen_id == data['project_id']).all()
        print(len(columndata))
        for row in columndata:
            row = { "id": row.id, "data": row.data }
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
    db.session.flush()


    # TODO: check for similary/duplicate projects by comparing attributes
    project_id = (CapsGen.find_by_id(id)).project_id
    project_in_gst_registration_table = GstRegistration.query.filter(GstRegistration.project_id == project_id).first()
    if project_in_gst_registration_table is not None:
        db.session.delete(project_in_gst_registration_table)
        db.session.commit()
    lfa1_result = SapLfa1.query.filter_by(capsgen_id=id).first()
    if lfa1_result is not None:
        gst_registration = GstRegistration(project_id=project_id, capsgen_id=id, vendor_country=fa1.data['LAND1'], vendor_number=fa1.data['LIFNR'], vendor_city=fa1.data['ORT01'], vendor_region=fa1.data['REGIO'])
        db.session.add(gst_registration)
        db.session.flush()
    else:
        raise ValueError("LFA1 does not exist, please run caps gen first.")

    db.session.commit()
    return jsonify(response), 200

#===============================================================================
# View Tables Page
@caps_gen.route('/<int:id>/view_tables/<path:table>', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def view_tables(id, table):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))

    # capsgen_id = CapsGen.query.filter(CapsGen.project_id == project_id).order_by(desc(CapsGen.id)).first().id
    # if not capsgen_id:
    #     raise ValueError('CAPS Generation has not been run on this project yet. Please run CAPS Generation from source data upload.')

    #table filter
    tableclass = eval('Sap' + str(table.lower().capitalize()))
    columndata = tableclass.query.with_entities(getattr(tableclass, 'data')).filter(tableclass.caps_gen_id == id).all()
    response['payload'] = columndata
    response['message'] = ''
    return jsonify(response), 200

#===============================================================================
# Data Quality Check
# this performs 3 quality checks - checking for validity (regex), completeness
# (nulls/total cols), uniqueness (uniqueness of specified key grouping from data
# dictionary)
@caps_gen.route('/<int:id>/data_quality_check', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def data_quality_check(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))

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

    data = request.get_json()
    CDM_query = [label.serialize for label in CDMLabel.query.all()]
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
                row = [row.data[x] for x in unique_keys]
                ''.join(row)
                unique_key_checker.append(row)
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
            query = [row.data[column] for row in data]
            if compiled_data_dictionary[column]['regex']:
                data_dictionary_results[table][column] = {
                    'regex': validity_check(query, compiled_data_dictionary[column]['regex'])}
        ###completeness check ###
            data_dictionary_results[table][column] = {
                'completeness': completeness_check(query)}
    response['payload'] = data_dictionary_results
    return jsonify(response), 200

#===============================================================================
# Data to APS
# j1 to j10 joins to create APS j1_j10
@caps_gen.route('/<int:id>/data_to_aps', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def data_to_aps(id):
    response = { 'status': 'ok', 'message': {}, 'payload': {} }
    # response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))
    project_id = (query.first()).projet_id

    def execute(query):
        # print(str(datetime.datetime.now()))
        # print("Executing...")
        result = db.session.execute(query)
        # print("Committing...")
        db.session.commit()
        # print("Done.")
        # return 'query execute successful'
        return


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
        INTO APS
        FROM J2_BSEG_BKPF_LFA1 AS L
        INNER JOIN distinctVarAPKey AS R
        ON L.varAPKey = R.varAPKey
        """

        j11 = """
        select L.*,
        R.data ->> 't001_bukrs_key' as t001_bukrs_key,
        R.data ->> 'co_name' as co_name,
        R.data ->> 'KTOPL'  as t001_ktopl
        from (select * from j3_BSEG_BKPF_LFA1_OnlyAP where cast(data ->> 'fiscal_year_gl' as text) = '2013') as L
        left join (select * from sap_t001 where capsgen_id = {capsgen_id}) as R
        on L.data ->> 'co_code_gl' = R.data ->> 't001_bukrs_key
        """.format(capsgen_id = capsgen_id)

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
    return jsonify(response), 200

#===============================================================================
# View APS Page
@caps_gen.route('/<int:id>/view_aps', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def view_aps(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))

    response['payload'] = [SapAps.query.filter_by(caps_gen_id = id).all()]
    return jsonify(response), 200

#===============================================================================
# APS Quality Check
# This is the check that needs to be done to see whether vardocamt and varlocamt
# net to 0. This is referring to GL netting to 0. Ask Andy for more details.
@caps_gen.route('/<int:id>/aps_quality_check', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def aps_quality_check(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))
    project_id = (query.first()).projet_id

    # TODO: APS QUALITY CHECK AND GL NET CHECK

    return jsonify(response), 200

#===============================================================================
# APS to CAPS
# see feature branch 72-aps_to_caps for more info
@caps_gen.route('/<int:id>/aps_to_caps', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def aps_to_caps(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))
    project_id = (query.first()).projet_id

    def execute(query):
        # print(str(datetime.datetime.now()))
        # print("Executing...")
        result = db.session.execute(query)
        # print("Committing...")
        db.session.commit()
        # print("Done.")
        # return 'query execute successful'
        return

    j17 = """
        drop table if exists aps_relational;
    select
    L.data ->> 'MANDT' as MANDT,
    L.data ->> 'BUZID' as BUZID,
    L.data ->> 'AUGDT' as AUGDT,
    L.data ->> 'AUGCP' as AUGCP,
    L.data ->> 'AUGBL' as AUGBL,
    L.data ->> 'KOART' as KOART,
    L.data ->> 'UMSKZ' as UMSKZ,
    L.data ->> 'UMSKS' as UMSKS,
    L.data ->> 'ZUMSK' as ZUMSK,
    L.data ->> 'SHKZG' as SHKZG,
    L.data ->> 'QSSKZ' as QSSKZ,
    L.data ->> 'KZBTR' as KZBTR,
    L.data ->> 'PSWBT' as PSWBT,
    L.data ->> 'PSWSL' as PSWSL,
    L.data ->> 'HWBAS' as HWBAS,
    L.data ->> 'TXGRP' as TXGRP,
    L.data ->> 'KTOSL' as KTOSL,
    L.data ->> 'QSSHB' as QSSHB,
    L.data ->> 'ZUONR' as ZUONR,
    L.data ->> 'VBUND' as VBUND,
    L.data ->> 'BEWAR' as BEWAR,
    L.data ->> 'VORGN' as VORGN,
    L.data ->> 'AUFNR' as AUFNR,
    L.data ->> 'ANBWA' as ANBWA,
    L.data ->> 'XUMSW' as XUMSW,
    L.data ->> 'XCPDD' as XCPDD,
    L.data ->> 'XAUTO' as XAUTO,
    L.data ->> 'XZAHL' as XZAHL,
    L.data ->> 'SAKNR' as SAKNR,
    L.data ->> 'XBILK' as XBILK,
    L.data ->> 'GVTYP' as GVTYP,
    L.data ->> 'ZFBDT' as ZFBDT,
    L.data ->> 'ZTERM' as ZTERM,
    L.data ->> 'ZBD1T' as ZBD1T,
    L.data ->> 'ZBD2T' as ZBD2T,
    L.data ->> 'ZBD3T' as ZBD3T,
    L.data ->> 'ZBD1P' as ZBD1P,
    L.data ->> 'ZBD2P' as ZBD2P,
    L.data ->> 'SKFBT' as SKFBT,
    L.data ->> 'SKNTO' as SKNTO,
    L.data ->> 'ZLSCH' as ZLSCH,
    L.data ->> 'NEBTR' as NEBTR,
    L.data ->> 'REBZG' as REBZG,
    L.data ->> 'REBZJ' as REBZJ,
    L.data ->> 'REBZZ' as REBZZ,
    L.data ->> 'QSFBT' as QSFBT,
    L.data ->> 'WERKS' as WERKS,
    L.data ->> 'MENGE' as MENGE,
    L.data ->> 'MEINS' as MEINS,
    L.data ->> 'ERFME' as ERFME,
    L.data ->> 'BWKEY' as BWKEY,
    L.data ->> 'BWTAR' as BWTAR,
    L.data ->> 'BUSTW' as BUSTW,
    L.data ->> 'STCEG' as STCEG,
    L.data ->> 'EGLLD' as EGLLD,
    L.data ->> 'XHKOM' as XHKOM,
    L.data ->> 'NPLNR' as NPLNR,
    L.data ->> 'AUFPL' as AUFPL,
    L.data ->> 'APLZL' as APLZL,
    L.data ->> 'DMBE2' as DMBE2,
    L.data ->> 'HWMET' as HWMET,
    L.data ->> 'XRAGL' as XRAGL,
    L.data ->> 'XNEGP' as XNEGP,
    L.data ->> 'KIDNO' as KIDNO,
    L.data ->> 'FKBER_LONG' as FKBER_LONG,
    L.data ->> 'AUGGJ' as AUGGJ,
    L.data ->> 'SEGMENT' as SEGMENT,
    L.data ->> 'TAXPS' as TAXPS,
    L.data ->> 'main_asset_num' as main_asset_num,
    L.data ->> 'asset_sub_num' as asset_sub_num,
    L.data ->> 'gl_doc_num' as gl_doc_num,
    L.data ->> 'post_key_gl' as post_key_gl,
    L.data ->> 'co_code_gl' as co_code_gl,
    L.data ->> 'bseg_buzei_key' as bseg_buzei_key,
    L.data ->> 'amount_local_ccy' as amount_local_ccy,
    L.data ->> 'po_doc_num' as po_doc_num,
    L.data ->> 'bseg_ebelp_key' as bseg_ebelp_key,
    L.data ->> 'func_area_gl' as func_area_gl,
    L.data ->> 'fiscal_year_gl' as fiscal_year_gl,
    L.data ->> 'bus_area_dept_num_gl' as bus_area_dept_num_gl,
    L.data ->> 'largest_debit_half_acct_num_gl' as largest_debit_half_acct_num_gl,
    L.data ->> 'cost_ctr_num_gl' as cost_ctr_num_gl,
    L.data ->> 'cx_num' as cx_num,
    L.data ->> 'material_num_gl' as material_num_gl,
    L.data ->> 'po_tax_code_gl' as po_tax_code_gl,
    L.data ->> 'gst_hst_qst_pst_local_ccy' as gst_hst_qst_pst_local_ccy,
    L.data ->> 'bseg_pargb_key' as bseg_pargb_key,
    L.data ->> 'profit_ctr_num' as profit_ctr_num,
    L.data ->> 'wbs_gl' as wbs_gl,
    L.data ->> 'item_descr_gl' as item_descr_gl,
    L.data ->> 'tax_jur_gl' as tax_jur_gl,
    L.data ->> 'sales_doc_num_gl' as sales_doc_num_gl,
    L.data ->> 'billing_doc_num' as billing_doc_num,
    L.data ->> 'gst_hst_pst_qst_doc_ccy' as gst_hst_pst_qst_doc_ccy,
    L.data ->> 'ap_ar_amt_doc_ccy' as ap_ar_amt_doc_ccy,
    L.varapkey,
    L.vend_num,
    L.varmultivnd,
    L.doc_type_gl,
    L.inv_date,
    L.inv_num,
    L.ccy,
    L.fiscal_period_gl,
    L.cputm,
    L.fx_rate,
    L.trnx_code_gl,
    L.ktopl,
    L.vend_name,
    L.name2,
    L.lfa1_land1_key,
    L.vend_region,
    L.vend_city,
    L.pstlz,
    L.stras,
    R.vardocamt,
    R.varlocamt
    into aps_relational
    from
    aps as L
    left join
    (select id,
     -(cast(data ->> 'ap_ar_amt_doc_ccy' as FLOAT)) as vardocamt,
     -(cast(data ->> 'amount_local_ccy' as FLOAT)) as varlocamt
     from aps where cast(data ->> 'SHKZG' as TEXT) = 'H') as R on L.id = R.id
    """.format(project_id = data['project_id'])

        #Generates raw account sum, groups varaccountcode and varapkey, sums on dmbtr, wrbtr, pswbt, dmbe2, vardocamt, and varlocamt. retrieves first row num for everything else. order by vartranamount
    j18 = """
        DROP TABLE IF EXISTS aps_acct_summ;
        SELECT
        *
        INTO aps_acct_summ
        FROM
        (
        SELECT
         Sum(Cast(amount_local_ccy AS FLOAT)) AS amount_local_ccy,
         Sum(Cast(ap_ar_amt_doc_ccy AS FLOAT)) AS ap_ar_amt_doc_ccy,
         Sum(Cast(pswbt AS FLOAT)) AS PSWBT,
         Sum(Cast(dmbe2 AS FLOAT)) AS DMBE2,
        SUM(vardocamt) as vardocamt,
        SUM(varlocamt) as varlocamt,

         l.varapkey,
         Trim(largest_debit_half_acct_num_gl) AS varaccountcode
        FROM
         aps_relational AS l
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
				Trim(largest_debit_half_acct_num_gl) AS varaccountcode_temp,
            MANDT,
            BUZID,
            AUGDT,
            AUGCP,
            AUGBL,
            KOART,
            UMSKZ,
            UMSKS,
            ZUMSK,
            SHKZG,
            QSSKZ,
            KZBTR,
            PSWSL,
            HWBAS,
            TXGRP,
            KTOSL,
            QSSHB,
            ZUONR,
            VBUND,
            BEWAR,
            VORGN,
            AUFNR,
            ANBWA,
            XUMSW,
            XCPDD,
            XAUTO,
            XZAHL,
            SAKNR,
            XBILK,
            GVTYP,
            ZFBDT,
            ZTERM,
            ZBD1T,
            ZBD2T,
            ZBD3T,
            ZBD1P,
            ZBD2P,
            SKFBT,
            SKNTO,
            ZLSCH,
            NEBTR,
            REBZG,
            REBZJ,
            REBZZ,
            QSFBT,
            WERKS,
            MENGE,
            MEINS,
            ERFME,
            BWKEY,
            BWTAR,
            BUSTW,
            STCEG,
            EGLLD,
            XHKOM,
            NPLNR,
            AUFPL,
            APLZL,
            HWMET,
            XRAGL,
            XNEGP,
            KIDNO,
            FKBER_LONG,
            AUGGJ,
            SEGMENT,
            TAXPS,
            main_asset_num,
            asset_sub_num,
            gl_doc_num,
            post_key_gl,
            co_code_gl,
            bseg_buzei_key,
            po_doc_num,
            bseg_ebelp_key,
            func_area_gl,
            fiscal_year_gl,
            bus_area_dept_num_gl,
            largest_debit_half_acct_num_gl,
            cost_ctr_num_gl,
            cx_num,
            vend_num,
            material_num_gl,
            po_tax_code_gl,
            gst_hst_qst_pst_local_ccy,
            bseg_pargb_key,
            profit_ctr_num,
            wbs_gl,
            item_descr_gl,
            tax_jur_gl,
            sales_doc_num_gl,
            billing_doc_num,
            gst_hst_pst_qst_doc_ccy,
             varmultivnd,
             doc_type_gl,
            inv_date,
             inv_num,
             ccy,
             fiscal_period_gl,
             cputm,
             fx_rate,
             trnx_code_gl,
             ktopl,
             vend_name,
             name2,
             lfa1_land1_key,
             vend_region,
             vend_city,
             pstlz,
             stras,

            Row_number() OVER( partition BY varapkey, Trim(largest_debit_half_acct_num_gl)
            ORDER BY
            MANDT,
            BUZID,
            AUGDT,
            AUGCP,
            AUGBL,
            KOART,
            UMSKZ,
            UMSKS,
            ZUMSK,
            SHKZG,
            QSSKZ,
            KZBTR,
            PSWSL,
            HWBAS,
            TXGRP,
            KTOSL,
            QSSHB,
            ZUONR,
            VBUND,
            BEWAR,
            VORGN,
            AUFNR,
            ANBWA,
            XUMSW,
            XCPDD,
            XAUTO,
            XZAHL,
            SAKNR,
            XBILK,
            GVTYP,
            ZFBDT,
            ZTERM,
            ZBD1T,
            ZBD2T,
            ZBD3T,
            ZBD1P,
            ZBD2P,
            SKFBT,
            SKNTO,
            ZLSCH,
            NEBTR,
            REBZG,
            REBZJ,
            REBZZ,
            QSFBT,
            WERKS,
            MENGE,
            MEINS,
            ERFME,
            BWKEY,
            BWTAR,
            BUSTW,
            STCEG,
            EGLLD,
            XHKOM,
            NPLNR,
            AUFPL,
            APLZL,
            HWMET,
            XRAGL,
            XNEGP,
            KIDNO,
            FKBER_LONG,
            AUGGJ,
            SEGMENT,
            TAXPS,
            main_asset_num,
            asset_sub_num,
            gl_doc_num,
            post_key_gl,
            co_code_gl,
            bseg_buzei_key,
            po_doc_num,
            bseg_ebelp_key,
            func_area_gl,
            fiscal_year_gl,
            bus_area_dept_num_gl,
            largest_debit_half_acct_num_gl,
            cost_ctr_num_gl,
            cx_num,
            material_num_gl,
            po_tax_code_gl,
            gst_hst_qst_pst_local_ccy,
            bseg_pargb_key,
            profit_ctr_num,
            wbs_gl,
            item_descr_gl,
            tax_jur_gl,
            sales_doc_num_gl,
            billing_doc_num,
            gst_hst_pst_qst_doc_ccy,
             vend_num,
             varmultivnd,
             doc_type_gl,
            inv_date,
             inv_num,
             ccy,
             fiscal_period_gl,
             cputm,
             fx_rate,
             trnx_code_gl,
             ktopl,
             vend_name,
             name2,
             lfa1_land1_key,
             vend_region,
             vend_city,
             pstlz,
             stras
             DESC) AS roworder
               FROM
                  aps_relational
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
        DROP TABLE IF EXISTS aps_tax_calc;
        select case when sel_acct = 'G' then varlocamt else 0 end as GST_HST ,
        case when sel_acct = 'P' then varlocamt else 0 end as PST,
        case when sel_acct = 'P_SA' then varlocamt else 0 end as PST_SA,
        case when sel_acct = 'O' then varlocamt else 0 end as TAXES_OTHER,
        case when sel_acct = 'Q' then varlocamt else 0 end as QST,
        case when sel_acct = 'A' then varlocamt else 0 end as AP_AMT,
        *
        into aps_tax_calc
        from (
        select
        case when varaccountcode in ('0000140500','0000220040') then 'G'
        when varaccountcode in ('NA') then 'P'
        when varaccountcode in ('0000220080') then 'P_SA'
        when varaccountcode in ('NA') then 'O'
        when varaccountcode in ('NA') then 'Q'
        when varaccountcode in ('0000210010',
        '0000210025',
        '0000210030',
        '0000210050',
        '0000210070',
        '0000210090',
        '0000210110'
        ) then 'A'
        else ''
        end as SEL_ACCT,
            *
        from
        aps_acct_summ
            ) as subq
      """

    j20 = """
               DROP TABLE IF EXISTS aps_summ;
    SELECT
       *
       INTO aps_summ
    FROM
       (
          SELECT
             Sum(Cast(amount_local_ccy AS FLOAT)) AS amount_local_ccy,
             Sum(Cast(ap_ar_amt_doc_ccy AS FLOAT)) AS ap_ar_amt_doc_ccy,
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
                   MANDT,
                    BUZID,
                    AUGDT,
                    AUGCP,
                    AUGBL,
                    KOART,
                    UMSKZ,
                    UMSKS,
                    ZUMSK,
                    SHKZG,
                    QSSKZ,
                    KZBTR,
                    PSWSL,
                    HWBAS,
                    TXGRP,
                    KTOSL,
                    QSSHB,
                    ZUONR,
                    VBUND,
                    BEWAR,
                    VORGN,
                    AUFNR,
                    ANBWA,
                    XUMSW,
                    XCPDD,
                    XAUTO,
                    XZAHL,
                    SAKNR,
                    XBILK,
                    GVTYP,
                    ZFBDT,
                    ZTERM,
                    ZBD1T,
                    ZBD2T,
                    ZBD3T,
                    ZBD1P,
                    ZBD2P,
                    SKFBT,
                    SKNTO,
                    ZLSCH,
                    NEBTR,
                    REBZG,
                    REBZJ,
                    REBZZ,
                    QSFBT,
                    WERKS,
                    MENGE,
                    MEINS,
                    ERFME,
                    BWKEY,
                    BWTAR,
                    BUSTW,
                    STCEG,
                    EGLLD,
                    XHKOM,
                    NPLNR,
                    AUFPL,
                    APLZL,
                    HWMET,
                    XRAGL,
                    XNEGP,
                    KIDNO,
                    FKBER_LONG,
                    AUGGJ,
                    SEGMENT,
                    TAXPS,
                    main_asset_num,
                    asset_sub_num,
                    gl_doc_num,
                    post_key_gl,
                    co_code_gl,
                    bseg_buzei_key,
                    po_doc_num,
                    bseg_ebelp_key,
                    func_area_gl,
                    fiscal_year_gl,
                    bus_area_dept_num_gl,
                    largest_debit_half_acct_num_gl,
                    cost_ctr_num_gl,
                    cx_num,
                    material_num_gl,
                    po_tax_code_gl,
                    gst_hst_qst_pst_local_ccy,
                    bseg_pargb_key,
                    profit_ctr_num,
                    wbs_gl,
                    item_descr_gl,
                    tax_jur_gl,
                    sales_doc_num_gl,
                    billing_doc_num,
                    gst_hst_pst_qst_doc_ccy,
                     varmultivnd,
                     doc_type_gl,
                    inv_date,
                     inv_num,
                     ccy,
                     fiscal_period_gl,
                     cputm,
                     fx_rate,
                     trnx_code_gl,
                     ktopl,
                     vend_name,
                     name2,
                     lfa1_land1_key,
                     vend_region,
                     vend_city,
                     pstlz,
                     stras,

    				      Row_number() OVER( partition BY varapkey
                   ORDER BY
    				MANDT,
                    BUZID,
                    AUGDT,
                    AUGCP,
                    AUGBL,
                    KOART,
                    UMSKZ,
                    UMSKS,
                    ZUMSK,
                    SHKZG,
                    QSSKZ,
                    KZBTR,
                    PSWSL,
                    HWBAS,
                    TXGRP,
                    KTOSL,
                    QSSHB,
                    ZUONR,
                    VBUND,
                    BEWAR,
                    VORGN,
                    AUFNR,
                    ANBWA,
                    XUMSW,
                    XCPDD,
                    XAUTO,
                    XZAHL,
                    SAKNR,
                    XBILK,
                    GVTYP,
                    ZFBDT,
                    ZTERM,
                    ZBD1T,
                    ZBD2T,
                    ZBD3T,
                    ZBD1P,
                    ZBD2P,
                    SKFBT,
                    SKNTO,
                    ZLSCH,
                    NEBTR,
                    REBZG,
                    REBZJ,
                    REBZZ,
                    QSFBT,
                    WERKS,
                    MENGE,
                    MEINS,
                    ERFME,
                    BWKEY,
                    BWTAR,
                    BUSTW,
                    STCEG,
                    EGLLD,
                    XHKOM,
                    NPLNR,
                    AUFPL,
                    APLZL,
                    HWMET,
                    XRAGL,
                    XNEGP,
                    KIDNO,
                    FKBER_LONG,
                    AUGGJ,
                    SEGMENT,
                    TAXPS,
                    main_asset_num,
                    asset_sub_num,
                    gl_doc_num,
                    post_key_gl,
                    co_code_gl,
                    bseg_buzei_key,
                    po_doc_num,
                    bseg_ebelp_key,
                    func_area_gl,
                    fiscal_year_gl,
                    bus_area_dept_num_gl,
                    largest_debit_half_acct_num_gl,
                    cost_ctr_num_gl,
                    cx_num,
                    vend_num,
                    material_num_gl,
                    po_tax_code_gl,
                    gst_hst_qst_pst_local_ccy,
                    bseg_pargb_key,
                    profit_ctr_num,
                    wbs_gl,
                    item_descr_gl,
                    tax_jur_gl,
                    sales_doc_num_gl,
                    billing_doc_num,
                    gst_hst_pst_qst_doc_ccy,
                     vend_num,
                     varmultivnd,
                     doc_type_gl,
                    inv_date,
                     inv_num,
                     ccy,
                     fiscal_period_gl,
                     cputm,
                     fx_rate,
                     trnx_code_gl,
                     ktopl,
                     vend_name,
                     name2,
                     lfa1_land1_key,
                     vend_region,
                     vend_city,
                     pstlz,
                     stras

                       DESC) AS roworder
    									   FROM
                      aps_tax_calc
                )
                AS subq
             WHERE
                subq.roworder = 1
          )
          AS r
          ON l.varapkey = r.varapkey_temp
    	  order by varlocamt desc
  """
    return jsonify(response), 200

@exception_wrapper()
def caps_to_erd_1():
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
    on L.post_key_gl = R.data ->> 'tbslt_bschl_key'
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
    #Join T005S: GRIRG does not exist
    # j18 = """
    # drop table if exists caps_3;
    #
    # select   L.*,
    # R.data ->> 't005s_bland_key' as t005s_bland_key,
    # R.data ->> 'prov_tx_code_tx' as prov_tx_code_tx,
    # R.data ->> 't005s_land1_key' as t005s_land1_key
    # into caps_3
    # from caps_2 as L
    # left join (select * from sap_t005s where capsgen_id = {capsgen_id}) as R
    # on L.data ->> 'GRIRG' = R.data ->> 't005s_bland_key'
    # """
    #Join CSKS to CSKT
    j19 = """
    drop table if exists j1_csks_cskt;

    select L.data ->> 'csks_kokrs_key' as csks_kokrs_key,
    L.data ->> 'csks_kostl_key' as csks_kostl_key,
    L.data ->> 'csks_datbi_key' as csks_datbi_key,
    L.data ->> 'cost_ctr_tx_jur' as cost_ctr_tx_jur,
    R.data ->> 'cskt_spras_key' as cskt_spras_key,
    R.data ->> 'cskt_kokrs_key' as cskt_kokrs_key,
    R.data ->> 'cskt_datbi_key' as cskt_datbi_key,
    R.data ->> 'cskt_kostl_key' as cskt_kostl_key,
    R.data ->> 'cost_ctr_name' as cost_ctr_name,
    R.data ->> 'cost_ctr_descr' as cost_ctr_descr
    into j1_csks_cskt
    from (select * from sap_csks where capsgen_id = {capsgen_id}) as L
    left join (select * from sap_cskt where capsgen_id = {capsgen_id}) as R
    on L.data ->> 'csks_kokrs_key' = R.data ->> 'cskt_kokrs_key'
    and L.data ->> 'csks_kostl_key' = R.data ->> 'cskt_kostl_key'
    """
    # #join CAPS to CSKS CSKT #control_area_gl does not exist
    j20 = """
    drop table if exists caps_4;
    select L.*,
    R.*
    into caps_4
    from (select * from caps_3) as L
    left join (select * from j1_csks_cskt) as R
    on L.control_area_gl = R.csks_kokrs_key
    """
    #join CEPC and CEPCT
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
    #join CAPS with j1_CEPC_CEPCT
    # j22 = """
    # drop table if exists caps_5;
    # select L.*,
    # R.*
    # into caps_5
    # from caps_4 as L
    # left join (select * from j1_CEPC_CEPCT) as R
    # on L.data ->> 'profit_ctr_num' = R.cepc_prctr_key
    # and L.data ->> 'bseg_budat_key' = R.cepc_datbi_key
    # #"""

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
    on L.wbs_gl = R.prps_pspnr_key
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
    # j29 = """
    # drop table if exists caps_5;
    # select L.*,
    # R.data ->> 'ttxjt_kalsm_key' as ttxjt_kalsm_key,
    # R.data ->> 'ttxjt_spras_key' as ttxjt_spras_key,
    # R.data ->> 'tx_jur_descr_tx' as tx_jur_descr_tx,
    # R.data ->> 'ttxjt_txjcd_key' as ttxjt_txjcd_key
    # into caps_5
    # from caps_4 as L
    # left join (select * from sap_ttxjt where capsgen_id = {capsgen_id}) as R
    # on L.tax_jur_gl = R.data ->> 'ttxjt_txjcd_key'
    # """.format(capsgen_id = capsgen_id)
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
    select L.*
    into j3_regup_t001_lfa1_ekpo
    from J2_REGUP_T001_LFA1 as L
    left join (select * from sap_ekpo where capsgen_id = {capsgen_id}) as R
    on L.regup_ebeln_key = R.data ->> 'ekpo_ebeln_key'
    and
    L.regup_ebelp_key = R.data ->> 'ekpo_ebelp_key'
    """

    j36 = """
    drop table if exists J3_SKB1_REGUP_T001_LFA1_EKPO;
    select L.data ->> 'ska1_bukrs_key' as skb1_bukrs_key,
    L.data ->> 'skb1_saknr_key' as skb1_saknr_key,
    R.*
    into J3_SKB1_REGUP_T001_LFA1_EKPO
    from (select * from sap_skb1 where capsgen_id = 9) as L
    left join (select * from j3_regup_t001_lfa1_ekpo) as R
    on L.data ->> 'skb1_bukrs_key' = R.regup_bukrs_key
    and
    L.data ->> 'skb1_saknr_key' = R.regup_saknr_key
    """
    #Join CAPS to SKB1 REGUP + tables, remove t001 table b/c duplicate
    j37 = """
    drop table if exists caps_5;
    select L.*,
    R.*
    into caps_5
    from caps_4 as L
    left join J3_SKB1_REGUP_T001_LFA1_EKPO as R
    on L.co_code_gl = R.skb1_bukrs_key
    and
    L.largest_debit_half_acct_num_gl = R.skb1_saknr_key
    """
    return jsonify(response), 200

@exception_wrapper()
def caps_to_erd_2():
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
    into j3_lfa1_lfm1_lfas_t005t
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
    R.data ->> 'bsak_augdt_key' as bsak_augdt_key,
    R.data ->> 'bsak_belnr_key' as bsak_belnr_key,
    R.data ->> 'bsak_bukrs_key' as bsak_bukrs_key,
    R.data ->> 'bsak_buzei_key' as bsak_buzei_key,
    R.data ->> 'bsak_gjahr_key' as bsak_gjahr_key,
    R.data ->> 'bsak_lifnr_key' as bsak_lifnr_key,
    R.data ->> 'spec_trnx_type_gl' as spec_trnx_type_gl,
    R.data ->> 'spec_indicator_gl' as spec_indicator_gl,
    R.data ->> 'cash_disc_percent_1_gl' as cash_disc_percent_1_gl,
    R.data ->> 'cash_disc_days_1_gl' as cash_disc_days_1_gl,
    R.data ->> 'cash_disc_percent_2_gl' as cash_disc_percent_2_gl,
    R.data ->> 'cash_disc_days_2_gl' as cash_disc_days_2_gl,
    R.data ->> 'pymt_period_gl' as pymt_period_gl,
    R.data ->> 'pymt_terms_gl' as pymt_terms_gl,
    R.data ->> 'assign_num_gl' as assign_num_gl
    into j4_lfa1_lfm1_lfas_t005t_bsak
    from j3_lfa_lfm1_lfas_t005t as L
    left join (select * from sap_bsak where capsgen_id = {capsgen_id}) as R
    on L.lfa1_lifnr_key = R.bsak_lifnr_key
    """
    #Join LFA1+LFM1+LFAS+T005T+bsak on CAPS
    #dropped vend name, vend_region, lfa1_land1_key, vend_city, lfa1_lifnr_key,
    j7 = """
    drop table if exists caps_6;
    select
    L.*,
    R.lfm1_ekorg_key,
    R.incoterms1,
    R.incoterms2,
    R.lfm1_lifnr_key,
    R.lfas_lifnr_key,
    R.lfas_land1_key,
    R.lfas_stceg_key,
    R.t005t_land1_key,
    R.cntry_name,
    R.t005t_spras_key,
    R.bsak_augbl_key,
    R.bsak_augdt_key,
    R.bsak_belnr_key,
    R.bsak_bukrs_key,
    R.bsak_buzei_key,
    R.bsak_gjahr_key,
    R.bsak_lifnr_key,
    R.spec_trnx_type_gl,
    R.spec_indicator_gl,
    R.cash_disc_percent_1_gl,
    R.cash_disc_days_1_gl,
    R.cash_disc_percent_2_gl,
    R.cash_disc_days_2_gl,
    R.pymt_period_gl,
    R.pymt_terms_gl,
    R.assign_num_gl
    into caps_6
    from caps_5 as L
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
    left join (select * from sap_tskmt where capsgen_id = {capsgen_id}) as R
    on L.data ->> 'mat_tx_class_mat' = R.data ->> 'tskmt_taxkm_key'
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
     on L.mara_matkl_key = R.data ->> 't023t_matkl_key';
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
    R.data ->> 'makt_matnr_key' as makt_matnr_key
    into J4_MARA_TSKMT_T023T_T006A_MAKT
    from J3_MARA_TSKMT_T023T_T006A as L
    left join (select * from sap_makt where capsgen_id = {capsgen_id}) as R
    on L.mara_matnr_key = R.data ->> 'makt_matnr_key'
    """
    #Join MLAN to T005T, remove T005t columns because they are duplicate
    j14 = """
        drop table if exists J1_MLAN_T005T;
    select
    L.data ->> 'mat_dept_ctry_mat' as mat_dept_ctry_mat,
    L.data ->> 'mlan_matnr_key' as mlan_matnr_key,
    L.data ->> 'mat_tx_ind_mat' as mat_tx_ind_mat,
    L.data ->> 'TAXM1' as TAXM1,
    L.data ->> 'TAXm2' as TAXM2
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
    drop table if exists caps_7;
    select
    L.*,
    R.*
    into caps_7
    from caps_6 as L
    left join J5_MARA_TSKMT_T023T_T006A_MAKT_MLAN_T005T as R
    on L.material_num_gl = R.mara_matnr_key
    """



    #removed T001W columns as they were duplicate
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
    L.data ->> 'umwrk' as umwrk
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
    L.data ->> 'handover_loc_po' as handover_loc_po,
    L.data ->> 'vend_phone' as vend_phone,
    L.data ->> 'vend_person' as vend_person,
    L.data ->> 'STCEG' as ekko_stceg_key,
    R.data ->> 't024e_ekorg_key' as t024e_ekorg_key,
    R.data ->> 'purch_org_descr_po' as purch_org_descr_po
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
    L.data ->> 'po_item_descr' as po_item_descr,
    R.data ->> 'stor_loc_desc_mat' as stor_loc_desc_mat,
    R.data ->> 'stor_loc_mat' as stor_loc_mat,
    R.data ->> 'stor_plant_mat' as stor_plant_mat
    into J1_EKPO_T001L
    from (select * from sap_ekpo where capsgen_id = {capsgen_id}) as L
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

    #Join EKPO T001L to TTXJT, but removed select fields because duplicate ttxjt
    j20 = """
    drop table if exists J2_EKPO_T001L_TTXJT;
    select
    L.*
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
    on L.ekpo_ebeln_key = R.mseg_ebeln_key
    AND
    L.ekpo_ebelp_key = R.mseg_ebelp_key
    """
    j21 = """
    drop table if exists J3_EKPO_T001L_TTXJT_MSEG_T001W_EKKO_T024E;
    select
    L.*,
    R.*
    into J3_EKPO_T001L_TTXJT_MSEG_T001W_EKKO_T024E
    from J3_EKPO_T001L_TTXJT_MSEG_T001W as L
    left join J1_EKKO_T024E as R
    on L.ekpo_ebeln_key = R.ekko_ebeln_key
    """

    j22 = """
    drop table if exists caps_8;
    select
    L.*,
    R.*
    into caps_8
    from caps_7 as L
    left join J3_EKPO_T001L_TTXJT_MSEG_T001W_EKKO_T024E as R
    on L.bseg_ebelp_key = R.ekpo_ebelp_key
	and L.po_doc_num = R.ekpo_ebeln_key
    """
    return jsonify(response), 200


@caps_gen.route('caps_calculations', methods=['POST'])
@exception_wrapper()
def caps_erd_calculations():
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
    return jsonify(response), 200

#===============================================================================
# View CAPS Page
@caps_gen.route('/<int:id>/view_caps', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def view_caps(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))

    # TODO: PULL FROM CAPS TABLES FILTER ON SPECIFIC CAPSGEN ID

    return jsonify(response), 200

#===============================================================================
# CAPS to Transactions
# This transforms all approved caps_gen tables to Transactions for the project
@caps_gen.route('/<int:id>/caps_to_transactions', methods=['GET'])
# @jwt_required
# @has_permission([])
@exception_wrapper()
def caps_to_transactions(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    capsgen = CapsGen.query.filter_by(id=id)
    if not capsgen.first():
        raise ValueError('CapsGen ID {} does not exist.'.format(id))
    project_id = (capsgen.first()).projet_id

    # TODO: transform caps to transactions

    capsgen.is_complete = True
    db.session.commit()
    return jsonify(response), 200
