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
import collections
import multiprocessing as mp
from anytree import Node, RenderTree
from collections import Counter
from azure.storage.file import FileService
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, current_user)
from os import path
from src.models import *
from config import *
from sqlalchemy import exists, desc, create_engine
from sqlalchemy.inspection import inspect
from src.caps_gen.creation import project_path_create, source_data_unzipper
from src.caps_gen.build_master import *
from src.caps_gen.data_quality_check import map_regex, recursive_find, recursive_insert
from src.caps_gen.to_aps import *
from src.caps_gen.to_caps import *
from src.errors import *
from src.util import validate_request_data, create_log
from src.wrappers import has_permission, exception_wrapper

caps_gen = Blueprint('caps_gen', __name__)
#===============================================================================
# GET ALL CAPS GEN
@caps_gen.route('/', defaults={'id':None}, methods=['GET'])
@caps_gen.route('/<int:id>', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_caps_gens(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query
    # ID filter
    if id is not None:
        query = query.filter_by(id=id)
        if not query.first():
            raise NotFoundError('ID {} does not exist.'.format(id))
    # Set ORDER
    query = query.order_by('created')
    # Set LIMIT
    query = query.filter_by(project_id = args['project_id']) if 'project_id' in args.keys() and args['project_id'].isdigit() else query
    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['message'] = ''
    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# DELETE A CAPS GEN
@caps_gen.route('/<int:id>', methods=['DELETE'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def delete_caps_gens(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = CapsGen.query.filter_by(id=id).first()
    if not query:
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    # TODO: make sure user deleting caps_gen is the user that made it!
    caps_gen = query.serialize
    db.session.delete(query)
    db.session.commit()
    # create_log(current_user, 'delete', 'CapsGen with id {}'.format(id), '')
    response['message'] = 'Deleted caps_gen id {}.'.format(caps_gen['id'])
    response['payload'] = [caps_gen]
    return jsonify(response), 200


#===============================================================================
#===============================================================================
#===============================================================================
# Project Path Creation
# creates project path in local file hierarchy for server
@caps_gen.route('/project_path_creation', methods=['POST'])
@jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def project_path_creation():
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()
    request_types = {
        'project_id': ['int'],
        'system': ['str']
    }
    validate_request_data(data, request_types)
    # TODO: If project path creation fails, we need to create rollback code.
    response = project_path_create(data, response)
    # create_log(current_user, 'create', 'Project path for CapsGen with project id {}'.format(data['project_id']), '')
    return jsonify(response), 200

#===============================================================================
# CapsGen Initialization
# unzips, creates CapsGen, creates DataMappings, builds master tables
@caps_gen.route('/init', methods=['POST'])
@jwt_required
@exception_wrapper()
# @has_permission([])
def init_caps_gen():
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()
    request_types = {
        'project_id': ['int'],
        'file_name': ['str'],
        'system': ['str']
    }
    validate_request_data(data, request_types)

    ### VALIDATE THAT NO CAPSGEN IS RUNNNING
    in_progress = CapsGen.query.filter_by(is_completed=False).first()
    if in_progress:
        raise InputError('Capsgen already in progress by user \'{}\' for project \'{}\''.format(in_progress.caps_gen_user.username if in_progress.caps_gen_user else 'None',in_progress.caps_gen_project.name))

    ### DO UNZIPPING
    try:
        source_data_unzipper(data, response) # pass filename here?
    except Exception as e:
        current_output_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
        list(map(os.unlink, (os.path.join(current_output_path, f) for f in os.listdir(current_output_path))))
        raise Exception(e)
    print('unzipping complete')


    ### CREATE CapsGen and DataMappings
    # TODO: change for project specific is_completed
    caps_gen = CapsGen(
        user_id=current_user.id,
        project_id=data['project_id']
    )
    db.session.add(caps_gen)
    db.session.flush()

    labels = [i.script_label for i in CDMLabel.query.all() if not i.is_calculated]
    for label in labels:
        new_mapping = DataMapping(
            caps_gen_id = caps_gen.id,
            cdm_label_script_label = label
        )
        db.session.add(new_mapping)
    db.session.commit()
    print('caps_gen model and data_mappings created')

    ### DO BUILD MASTER FILES
    try:
        ### DEV/PROD => make master tables
        list_tablenames = current_app.config['CDM_TABLES']
        N = mp.cpu_count()
        with mp.Pool(processes = N) as p:
           p.map(build_master_file, [ {'table': table, 'data': data} for table in list_tablenames])
        with mp.Pool(processes = N) as p:
           p.map(build_master_table, [ {'table': table, 'data': data, 'id': caps_gen.id} for table in list_tablenames])
        # engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
        # #todo: add table to payload so cio can know which tables to view
        # for table in list_tablenames:
        #     print(table)
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


        #     # for file in directory:
        #     #   get first line of file as headers
        #     #   build base dictionary with headers and blank data
        #     #   for each other line in file:
        #     #       take base dict and populate and add
        #     #       after 1000, commit

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
        #                 list_to_insert.append({"caps_gen_id": caps_gen.id, 'data': dict(zip(header, line.rstrip('\n').split('#|#')))})
        #         if counter > 0:
        #             engine.execute(referenceclass.__table__.insert(), list_to_insert)

        #     db.session.flush()
        ###

        # get data from blob and put into caps_gen tables

        #####

        db.session.commit()
        ## Remove data from caps_gen_master
        master_tables_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_MASTER_LOCATION'])
        list(map(os.unlink, (os.path.join(master_tables_path, f) for f in os.listdir(master_tables_path))))
        ## Remove data from caps_gen_unzipped
        current_output_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
        list(map(os.unlink, (os.path.join(current_output_path, f) for f in os.listdir(current_output_path))))
        response['message'] = 'Data successfully uploaded and CapsGen initialized.'
        response['payload'] = [CapsGen.find_by_id(caps_gen.id).serialize]
    except Exception as e:
        ## Remove data from caps_gen_master
        master_tables_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_MASTER_LOCATION'])
        list(map(os.unlink, (os.path.join(master_tables_path, f) for f in os.listdir(master_tables_path))))
        ## Remove data from caps_gen_unzipped
        current_output_path = os.path.join(os.getcwd(), current_app.config['CAPS_BASE_DIR'], str(data['project_id']), current_app.config['CAPS_UNZIPPING_LOCATION'])
        list(map(os.unlink, (os.path.join(current_output_path, f) for f in os.listdir(current_output_path))))
        # delete created caps_gen
        db.session.delete(caps_gen)
        db.session.commit()
        raise Exception(e)

    # create_log(current_user, 'create', 'Init for CapsGen with project id {}'.format(data['project_id']), '')

    return jsonify(response), 200

#===============================================================================
# Master Table headers  `table_name::column_name` list
# get master table data from caps_gen tables
@caps_gen.route('/<int:id>/master_table_headers', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_master_table_headers(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    mappings = [i.serialize for i in DataMapping.query.filter_by(caps_gen_id=id).all()]

    headers = []
    header_data = query.first().get_headers
    for key in header_data.keys():
        header = key.partition('sap')[2].lower()
        header_set = { header: [] }
        for item in header_data[key]:
            header_set[header].append({'table_name': header, 'column_name': item })
        headers.append(header_set)

    # def get_column_name(table, caps_data):
    #     return [{'table_name': table, 'column_name': header } for header in caps_data]
    #
    # headers = [{table.partition('sap')[2].lower(): list(itertools.chain.from_iterable(list(map(lambda x: get_column_name(table.partition('sap')[2].lower(), x), value))))} for table, value in query.first().get_headers['caps_data'].items()]
    for mapping in mappings:
        if mapping['table_column_name']:
            for header in headers:
                header.update({list(header.keys())[0]: [x for x in header[list(header.keys())[0]] if x != mapping['table_column_name'][0]]})


    response['payload'] = headers

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
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def apply_mappings_build_gst_registration(id):
    response = {'status': 'ok', 'message': '', 'payload': []}
    data = request.get_json()
    request_types = {
        'project_id': ['int'],
        'file_name': ['str'],
        'system': ['str']
    }
    validate_request_data(data, request_types)

    # APPLY MAPPINGS
    mappings = [i for i in DataMapping.query.filter_by(caps_gen_id = id).all() if i.serialize['table_column_name']]
    mappables = {}
    for mapping in mappings:
        table_to_modify = "Sap"+(mapping.table_name).lower().capitalize()
        if table_to_modify not in mappables.keys():
            mappables[table_to_modify] = []
        mappables[table_to_modify].append((mapping.column_name, mapping.cdm_label_script_label))

    N = mp.cpu_count()
    with mp.Pool(processes = N) as p:
        p.map(apply_mapping, [ {'table': key, 'label': value, 'id': id} for key, value in mappables.items()])
    # for key in mappables.keys():
    #     print(key)
    #     limit = 100000
    #     offset = 0

    #     def map_data(limit, offset):
    #         query = [i for i in eval(key).query.filter_by(caps_gen_id=id).order_by('id').limit(limit).offset(offset).all()]
    #         print(len(query))
    #         for row in query:
    #             newdata = dict(row.data)
    #             for map in mappables[key]:
    #                 if map[0] in newdata.keys():
    #                     newdata[map[1]] = newdata.pop(map[0])
    #                 # print(newdata)
    #                 row.data = newdata
    #         db.session.commit()
    #         return len(query)
    #     qlen = 1
    #     while qlen > 0:
    #         qlen = map_data(limit, offset)
    #         offset += limit

    # BUILD GST REGISTRATION
    #TODO: V2 check for similary/duplicate projects by comparing attributesh
    # gst_data = [i.data for i in SapLfa1.query.filter_by(caps_gen_id=id).all()]
    # for vendor in gst_data:
    #     if [x for x in ['lfa1_land1_key','lfa1_lifnr_key','vend_city','vend_region'] if x not in vendor.keys()]:
    #         raise NotFoundError("Err during GST Registration. Lfa1 table not complete.")
    #     gst_entry = GstRegistration(
    #         caps_gen_id = id,
    #         vendor_country=vendor['lfa1_land1_key'],
    #         vendor_number=vendor['lfa1_lifnr_key'],
    #         vendor_city=vendor['vend_city'],
    #         vendor_region=vendor['vend_region']
    #     )
    #     db.session.add(gst_entry)
    db.session.commit()

    # create_log(current_user, 'modify', 'Applied Data Mappings and built GST Registration for CapsGen with id {}'.format(id), '')
    response['message'] = 'Successfully applied mappings and added vendors to GST Registration table.'

    return jsonify(response), 200


#===============================================================================
# Get table names for View Tables Page
@caps_gen.route('/<int:id>/get_tables', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def get_tables(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    tables = query.first().get_tables

    response['payload'] = tables

    return jsonify(response), 200

#===============================================================================
# View Tables Page
@caps_gen.route('/<int:id>/view_tables/<path:table>', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def view_tables(id, table):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    #table filter
    tableclass = eval('Sap' + str(table.lower().capitalize()))
    print(tableclass)
    query = tableclass.query.filter_by(caps_gen_id = id)

    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.data for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# Data Quality Check
# this performs 3 quality checks - checking for validity (regex), completeness
# (nulls/total cols), uniqueness (uniqueness of specified key grouping from data
# dictionary)
@caps_gen.route('/<int:id>/data_quality_check', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def data_quality_check(id):

    response = { 'status': 'ok', 'message': '', 'payload': [] }

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    final_result = {'scores_per_table': {}}
    overall_completeness_score = 0
    overall_uniqueness_score = 0
    overall_datatype_score = 0
    mappings = [i for i in DataMapping.query.filter_by(caps_gen_id = id).all() if i.serialize['table_column_name']]

    if len(mappings) == 0:
        raise InputError('No header mapped can not run data quality check')

    for table_name, group in itertools.groupby(mappings,key=lambda x: x.table_name.lower()):

        # For edge case: check if there is any data in table if not pass the table
        data_query =  eval('Sap' + str(table_name.lower().capitalize())).query.filter_by(caps_gen_id = id)
        total_count = data_query.count()
        if total_count == 0:
            continue

        # paraparing data for processing
        mapped_columns = [ mapping.cdm_label_script_label  for mapping in group ]
        query = CDMLabel.query.filter(CDMLabel.script_label.in_(mapped_columns))
        unique_keys = [row[0] for row in query.with_entities(getattr(CDMLabel, 'script_label')).filter_by(is_unique = True).all()]
        datatypes = {row[0]: map_regex(row[1].name) for row in query.with_entities(getattr(CDMLabel, 'script_label'), getattr(CDMLabel, 'datatype')).all()}

        limit = 200000
        offset = 0
        rep = []
        dup_result = 0
        root = Node('~', count=0)
        completeness_score = { column_name : 0 for column_name in mapped_columns}
        datatypes_score = { column_name : 0 for column_name in mapped_columns}

        def check_quality(limit, offset):
            query = [i for i in data_query.order_by('id').limit(limit).offset(offset).all()]
            dup_result = 0
            try:
                for row in query:
                    # uniqueness
                    cancated_value = ''.join([row.data[unique_key] for unique_key in unique_keys])
                    if cancated_value:
                        found = recursive_find(root, cancated_value)
                        if found:
                            dup_result += 1
                            if cancated_value not in rep:
                                rep.append(cancated_value)
                        recursive_insert(root, cancated_value)

                     # completeness
                    for key, value in row.data.items():
                        if value and key in mapped_columns:
                            completeness_score[key] += 1
                            if re.match(datatypes[key], value):
                                datatypes_score[key] += 1

            except Exception as e:
                print("Exception {}".format(e))
                # raise Exception(e)
            return [len(query), dup_result]

        qlen = 1
        while qlen > 0:
            result = check_quality(limit, offset)
            qlen = result[0]
            dup_result += result[1]
            offset += limit

        temp_overall_completeness_score = 0
        temp_overall_datatype_score = 0
        # compute completeness_score
        completeness = []
        for key, value in completeness_score.items():
            score = value / total_count * 100
            completeness.append({"column_name": key, "score": score })
            temp_overall_completeness_score += score
        overall_completeness_score += temp_overall_completeness_score / len(completeness)

        datatype = []
        for key, value in datatypes_score.items():
            # score = value / completeness_score[key] * 100 if completeness_score[key] else 0
            score = value / total_count * 100
            datatype.append({"column_name": key, "score": score })
            temp_overall_datatype_score += score
        overall_datatype_score += temp_overall_datatype_score / len(datatype)

        uniqueness = (1 - dup_result / total_count) * 100
        overall_uniqueness_score += uniqueness

        final_result['scores_per_table'][table_name] = {
                                            'completeness': completeness,
                                            'uniqueness': {
                                                'score': uniqueness,
                                                'key_names': unique_keys,
                                                'repetitions': rep
                                                },
                                            'datatype': datatype
                                            }
    final_result['overalls'] = {
                        'completeness' : overall_completeness_score / len(final_result['scores_per_table']),
                        'uniqueness': overall_uniqueness_score / len(final_result['scores_per_table']),
                        'datatype': overall_datatype_score / len(final_result['scores_per_table'])
                        }

    #     # let db does the dirty work
    #     if len(unique_keys) > 0:
    #         # UNIQUENESS
    #         print('qqqqq')
    #         print(table_name)
    #         names = '||'.join(['cast(data ->> \''+ column +'\' as text)' for column in unique_keys])
    #         # uniqueness score
    #         uniquenss_score_query_string = '''
    #         select ROUND((count(distinct({column_names}))::decimal / count(*)::decimal), 2) as uniqueness_score from sap_{table_name} where caps_gen_id = {caps_gen_id};
    #         '''.format(column_names = names , table_name = table_name, caps_gen_id = id)
    #         u = db.session.execute(uniquenss_score_query_string).first()

    #         if float(u[0]) < 1:
    #             # uniqueness repetition
    #             repetition_query_string = '''
    #             select {column_names} as duplicate_results from sap_bseg where caps_gen_id = {caps_gen_id} group by {column_names} HAVING count(*) > 1
    #             '''.format(column_names = names, caps_gen_id = id)
    #             r = db.session.execute(repetition_query_string)
    #         r = []
    #         overall_uniqueness_score += float(u[0])
    #     else:
    #         print('bbbbbb')
    #         r = []
    #         u = []

    #     # COMPLETENESS & DATATYPE for each column
    #     completeness_result = []
    #     datatype_result = []
    #     table_completeness_score = 0
    #     table_datatype_score = 0
    #     for column_name, datatype in datatypes.items():
    #         regex = ''
    #         if datatype == 'dt_varchar':
    #             regex = '.*'
    #         elif datatype == 'dt_float':
    #             regex = '^(?:\-)?\d*\.{1}\d+$'
    #         elif datatype == 'dt_int':
    #             regex = '^(?:\-)?\d+$'
    #         elif datatype == 'dt_date':
    #             regex = '^(0[1-9]|1[012])\/(0[1-9]|[1-2][0-9]|3[01])\/\d{4}$'
    #         else:
    #             raise Exception('No regex implmented for the given data type: {}'.format(datatype))

    #         print('datatype q')
    #         datatype_quety_string = '''
    #         select round(count_check::decimal / count_total::decimal , 2) from (
    #         SELECT (select count(*) from sap_{table_name} where caps_gen_id = {caps_gen_id}) count_total, count(*) as count_check FROM sap_{table_name} WHERE caps_gen_id = {caps_gen_id} and data ->> '{column_name}' ~ '{regex}' ) as L
    #         '''.format(table_name = table_name, column_name = column_name, caps_gen_id = id, regex = regex)

    #         d = db.session.execute(datatype_quety_string).first()
    #         datatype_result.append({
    #                             'column_name': column_name,
    #                             'score': float(d[0])
    #                             })
    #         print('cp q')
    #         completeness_score_query_string = '''
    #         select ROUND(((count(*) - sum(case when cast(data ->> '{column_name}' as text) = '' then 1 else 0 end)))::decimal / count(*)::decimal, 2) count_nulls from sap_{table_name} where caps_gen_id = {caps_gen_id};
    #         '''.format(column_name = column_name, table_name = table_name, caps_gen_id = id)

    #         c = db.session.execute(completeness_score_query_string).first()
    #         completeness_result.append({
    #                         'column_name': column_name,
    #                         'score': float(c[0])
    #                         })


    #         table_completeness_score += float(c[0])
    #         table_datatype_score += float(d[0])

    #     overall_completeness_score += table_completeness_score / len(datatypes)
    #     overall_datatype_score += table_datatype_score / len(datatypes)

    #     final_result['scores_per_table'][table_name] = {
    #                                                 'completeness': completeness_result,
    #                                                 'uniqueness': {
    #                                                     'score': float(u[0]) if u else 1,
    #                                                     'key_names': unique_keys,
    #                                                     'repetitions':[rep[0] for rep in r if r]
    #                                                     },
    #                                                 'datatype': datatype_result
    #                                                 }

    # final_result['overalls'] = {
    #                     'completeness' : overall_completeness_score / len(final_result['scores_per_table']),
    #                     'uniqueness': overall_uniqueness_score / len(final_result['scores_per_table']),
    #                     'datatype': overall_datatype_score / len(final_result['scores_per_table'])
    #                     }

    # print(final_result)

    # table_names = [ 'sap_'+mapping.table_name.lower() for mapping in mappings]
    # for table_name in table_names:
    #     if mapping

    # query = query.with_entities(getattr(CDMLabel, 'script_label'), getattr(CDMLabel, 'datatype'))
    # unique_labels = query.filter_by(is_unique = True).all()
    # data_types = query.all()

    # def merge_dicts(dicts):
    #     res = collections.defaultdict(list)
    #     for d in dicts:
    #         for k, v in d.iteritems():
    #             res[k].append(v)
    #     return res
    # def data_dictionary(mapping, table):
    #     rename_dict = {}
    #     for index, elem in enumerate(mapping):
    #         if mapping[index]['mappings'][0]['table_name'] == table:
    #             rename_dict.update({mapping[index]['script_label']: {
    #                 'is_calculated': mapping[index]['is_calculated'],
    #                 'is_required': mapping[index]['is_required'],
    #                 'is_unique': mapping[index]['is_unique'],
    #                 'regex': mapping[index]['regex'],
    #             }})
    #     return rename_dict

    # def validity_check(result, regex):
    #     validity_response = {}
    #     results = list(filter(re.compile(regex).match, result))
    #     validity_response['results'] = results
    #     validity_response['final_score'] = 100 - (len(validity_response['results'])/len(column))
    #     return validity_response

    # def completeness_check(result):
    #     completeness_response = {}
    #     counter = 0
    #     results = [elem for elem in result if elem == '' or elem == None]
    #     completeness_response['final_score'] =  (len(results) / len(result)) * 100
    #     return completeness_response

    # response = {'status': 'ok', 'message': {}, 'payload': []}
    # data_dictionary_results = {}
    # # uniqueness_response = {}
    # mappings = [i for i in DataMapping.query.filter_by(caps_gen_id = id).all() if i.serialize['table_column_name']]
    #  CDMLabel.query.filter_by()
    # for mapping in mappings:
    #     table_to_check = "Sap"+(mapping.table_name).lower().capitalize()
    #     table_class = eval(table_to_check)
    #     data_dictionary_results[table_to_check] = {}
    #     data = [row.data for row in table_class.query.filter_by(caps_gen_id = id).all()]
    #     print(data)
    #     # data_in_table = table_class.query.with_entities(getattr(table_class, 'id'), getattr(table_class, 'data')).filter(
    #         # table_class.caps_gen_id == id).all()

    # # data = request.get_json()
    # cmd_labels = [label.serialize for label in CDMLabel.query.all()]
    # # unique_keys = { label["script_label"] : 0 for label in cmd_labels if label["is_unique"] is True }
    # # key_data_types = {  label["script_label"]: db.enum(label["datatype"])  for label in cmd_labels }
    # unique_keys = {'vegie':0}
    # key_data_types = {'vegie':}
    # print(key_data_types)
    # print(unique_keys)
    # # print(data_in_table)
    # merged_dicts = merge_dicts(data)
    # count_total = 0
    # count_failed_unique = 0
    # count_failed_datatype = 0
    # for k, values in merged_dicts:
    #     count_total += len(values)
    #     if len(values) > 1:
    #         count_failed_unique += len(values)
    #         # put data in result
    #     for value in values:
    #        if type(value) is not key_data_types[k]:
    #            count_failed_datatype += 1

    # print(merged_dicts)
        #  merge_dicts()
        # for unique_key in unique_keys:
        #     if unique_key in row.keys():
        #         unique_keys[unique_key] += 1


    # for table in list_tablenames:
    #     data_dictionary_results[table] = {}eval
    #     tableclass = eval('Sap' + str(table.lower().capitalize()))
    #     compiled_data_dictionary = data_dictionary(CDM_query, table)
    #     data = tableclass.query.with_entities(getattr(tableclass, 'id'), getattr(tableclass, 'data')).filter(
    #         tableclass.caps_gen_id == id).all()
    #     ### UNIQUENESS CHECK ###
    #     #The argument should be set to true when some of is_unique column in CDM labels is set to True.
    #     unique_keys = [x for x in compiled_data_dictionary if compiled_data_dictionary[x]['is_unique'] == False]
    #     if unique_keys:
    #         unique_key_checker = []
    #         for row in data:
    #             row = [row.data[x] for x in unique_keys]
    #             ''.join(row)
    #             unique_key_checker.append(row)
    #         c = Counter(map(tuple, unique_key_checker))
    #         dups = [k for k, v in c.items() if v > 1]
    #     #if there are no unique keys, line below will bug out, saying its not being referenced. This is because dups above never runs so the var does not initialize.
    #     if len(dups) > 1:
    #         uniqueness_response['results'] = dups
    #         uniqueness_response['final_score'] = 100 - (len(dups)/tableclass.query.count())
    #         data_dictionary_results[table] = {'uniqueness' : uniqueness_response}
    #     else:
    #         uniqueness_response['final_score'] = 100
    #         data_dictionary_results[table] = {'uniqueness': 100}
    #     ### validity check ###
    #     for column in compiled_data_dictionary.keys():
    #         query = [row.data[column] for row in data]
    #         if compiled_data_dictionary[column]['regex']:
    #             data_dictionary_results[table][column] = {
    #                 'regex': validity_check(query, compiled_data_dictionary[column]['regex'])}
    #     ###completeness check ###
    #         data_dictionary_results[table][column] = {
    #             'completeness': completeness_check(query)}

    # create_log(current_user, 'create', 'Ran Data Quality Check for CapsGen with id {}'.format(id), '')
    response['payload'] = final_result
    return jsonify(response), 200

#===============================================================================
# Data to APS
# j1 to j10 joins to create APS j1_j10
@caps_gen.route('/<int:id>/data_to_aps', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def data_to_aps(id):
    response = { 'status': 'ok', 'message': {}, 'payload': {} }
    # response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))
    project_id = (query.first()).project_id

    def execute(query):
        result = db.session.execute(query)
        db.session.commit()
        return
    execute(j1(id))
    execute(j2(id))
    execute(j3(id))
    execute(j4(id))
    execute(j5(id))
    execute(j6(id))
    execute(j7(id))
    execute(j8(id))
    execute(j9(id))
    execute(j10(id))
    execute(j10point5(id))

    # create_log(current_user, 'modify', 'Ran Data To Aps for CapsGen with id {}'.format(id), '')

    return jsonify(response), 200

#===============================================================================
# View APS Page
@caps_gen.route('/<int:id>/view_aps', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def view_aps(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    query = SapAps.query.filter_by(caps_gen_id = id)

    # Set LIMIT
    query = query.limit(args['limit']) if 'limit' in args.keys() and args['limit'].isdigit() else query.limit(1000)
    # Set OFFSET
    query = query.offset(args['offset']) if 'offset' in args.keys() and args['offset'].isdigit() else query.offset(0)

    response['payload'] = [i.serialize for i in query.all()]

    return jsonify(response), 200

#===============================================================================
# APS Quality Check
# This is the check that needs to be done to see whether vardocamt and varlocamt
# net to 0. This is referring to GL netting to 0. Ask Andy for more details.
@caps_gen.route('/<int:id>/aps_quality_check', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def aps_quality_check(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))
    project_id = (query.first()).project_id

    # TODO: APS QUALITY CHECK AND GL NET CHECK

    # create_log(current_user, 'create', 'Ran APS Quality Check for CapsGen with id {}'.format(id), '')

    return jsonify(response), 200

#===============================================================================
# APS to CAPS
# see feature branch 72-aps_to_caps for more info
@caps_gen.route('/<int:id>/aps_to_caps', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def aps_to_caps(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))
    project_id = (query.first()).project_id

    def execute(query):
        result = db.session.execute(query)
        db.session.commit()
        return
    execute(j11())
    execute(j12())
    execute(j13())
    execute(j14())

    execute(j15())
    execute(j16())
    # execute(j17())
    execute(j18())
    execute(j19())
    # execute(j20())
    # execute(j21())
    execute(j22())
    execute(j23())
    execute(j24())
    execute(j25())
    # execute(j26(id))
    # execute(j27())
    # execute(j28(id))
    # execute(j29(id))
    # execute(j30(id))
    # execute(j31())
    execute(j32(id))
    # execute(j33(id))
    # execute(j34())
    # execute(j35(id))
    execute(j36(id))
    # execute(j37(id))
    execute(j38(id))
    execute(j39(id))
    execute(j40())
    # execute(j41(id))
    execute(j42(id))
    execute(j43(id))
    execute(j44(id))
    # execute(j45(id))
    execute(j46(id))
    execute(j47())
    execute(j48(id))
    execute(j49(id))
    execute(j50(id))
    execute(j51(id))
    execute(j52(id))
    execute(j53())
    execute(j54())
    execute(j55(id))
    execute(j56(id))
    execute(j57(id))
    # execute(j58(id))
    execute(j59(id))
    execute(j60())
    execute(j61())
    execute(j62())
    execute(j63())
    execute(j64())
    execute(j65())

    # create_log(current_user, 'modify', 'Ran APS to Caps for CapsGen with id {}'.format(id), '')
    return jsonify(response), 200

#===============================================================================
# View CAPS Page
@caps_gen.route('/<int:id>/view_caps', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def view_caps(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()

    query = CapsGen.query.filter_by(id=id)
    if not query.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    # TODO: PULL FROM CAPS TABLES FILTER ON SPECIFIC CAPSGEN ID

    return jsonify(response), 200

#===============================================================================
# CAPS to Transactions
# This transforms all approved caps_gen tables to Transactions for the project
@caps_gen.route('/<int:id>/caps_to_transactions', methods=['GET'])
# @jwt_required
@exception_wrapper()
# @has_permission(['tax_practitioner','tax_approver','tax_master','data_master','administrative_assistant'])
def caps_to_transactions(id):
    response = { 'status': 'ok', 'message': '', 'payload': [] }
    args = request.args.to_dict()
    engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
    caps_gen = CapsGen.query.filter_by(id=id)
    if not caps_gen.first():
        raise NotFoundError('CapsGen ID {} does not exist.'.format(id))

    project_id = (caps_gen.first()).project_id
    print(project_id)
    print('it got here')
    if Transaction.query.filter_by(project_id=project_id).first():
        print('deleting')
        engine.execute('DELETE FROM TRANSACTIONS WHERE project_id = {}'.format(project_id))

    result = engine.execute('INSERT INTO transactions(data, project_id) select row_to_json(row) as data , {project_id} project_id from (select * from sap_caps) row;').format(project_id)




    caps_gen.is_complete = True
    db.session.commit()

    # create_log(current_user, 'create', 'Built transactions for CapsGen with id {}'.format(id), '')
    return jsonify(response), 200
