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
import pandas as pd
import random
import re
import shutil
import zipfile
import requests
import sqlalchemy
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

@sap_caps_gen.route('/build_master_tables', methods=['GET'])
def build_master_tables():
    mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
    def rename_builder(table):
        rename_dict = {}
        for index, elem in enumerate(mapping):
            if mapping[index]['mappings'][0]['table_name'] == table:
                rename_dict.update({mapping[index]['mappings'][0]['column_name']: mapping[index]['script_label']})
        return rename_dict
    list_tablenames = list(set([table['mappings'][0]['table_name'] for table in mapping]))
    list_tablenames = ['BKPF']
    print(list_tablenames)
    response = {'status': '', 'message': {}, 'payload': []}
    for table in list_tablenames:
        print(table)
        list_of_files = []
        basetable = {}
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
                    renaming_scheme = rename_builder(table)
                    for key in renaming_scheme.keys():
                        print(key, renaming_scheme[key])
                        first_line = first_line.replace(key, renaming_scheme[key])
                    print(first_line)
                    first_line = first_line.encode()

                    #   add header to wfd
                    wfd.write(first_line)
        #     #   add rest of file to wfd
                    wfd.write(fd.read().encode())
            else:
                # for all future files
                with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_unzipped', file)), 'r', encoding='utf-8-sig') as fd:
                    #   strip header
                    next(fd)
                    wfd.write(fd.read().encode())
        wfd.close()
        print('table renamed to')
        print(renaming_scheme.values())
        referenceclass = eval('Sap' + str(table.lower().capitalize()))
        print(referenceclass)
        exampledump = []

        with open(get_cwd(os.path.join('caps_gen_processing/caps_gen_master', '{}_MASTER.txt'.format(table))), 'r', encoding='utf-8-sig') as masterfile:
            for line in csv.DictReader((line.replace('#|#', 'ø') for line in masterfile), delimiter='ø', quoting=csv.QUOTE_NONE):
                try:
                    dict_you_want = {your_key: line[your_key] for your_key in renaming_scheme.values()}
                    print(dict_you_want)
                except Exception as e:
                    print('Missing column')
                    continue
                dict_you_want['project_id'] = 1
                exampledump.append(dict_you_want)

        db.session.bulk_insert_mappings(referenceclass, exampledump)
        db.session.commit()
        print('great success')
    return 'OK'

@sap_caps_gen.route('/data_quality_check', methods=['GET'])


def data_quality_check():

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

    def completeness_check(column):
        completeness_response = {}
        for index, elem in enumerate(column):
            if '' == elem or elem.isspace():
                completeness_response[str(index)] = elem
        completeness_response['final_score'] = 100 - (len(completeness_response)/len(column))
        return completeness_response

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
            unique_results = list(list(zip(*tableclass.query.with_entities(getattr(tableclass, 'varapkey')).group_by(getattr(tableclass, 'varapkey')).having(func.count(getattr(tableclass, 'varapkey')) > 1).all()))[0])
            if len(unique_results) > 1:
                uniqueness_response = {}
                uniqueness_response['results'] = unique_results
                uniqueness_response['final_score'] = 100 - (len(unique_results)/tableclass.query.count())
                data_dictionary_results[table] = {'uniqueness' : uniqueness_response}
        for column in compiled_data_dictionary.keys():
            print(column)
            query = tableclass.query
            query = query.with_entities(getattr(tableclass, column))
            query = query.order_by(getattr(tableclass, column))
            result = list(list(zip(*query.all()))[0])
            print(len(result))
            if compiled_data_dictionary[column]['is_required']:
                data_dictionary_results[table][column] = {'completeness' : completeness_check(result)}
            if compiled_data_dictionary[column]['regex']:
                data_dictionary_results[table][column] = {'regex': validity_check(result, compiled_data_dictionary[column]['regex'])}
    return data_dictionary_results

@sap_caps_gen.route('/j1', methods=['GET'])
def j1():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)

@sap_caps_gen.route('/j2', methods=['GET'])
def j2():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)

@sap_caps_gen.route('/j3', methods=['GET'])
def j3():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)

@sap_caps_gen.route('/aps_quality_check', methods=['GET'])
def aps_quality_check():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)