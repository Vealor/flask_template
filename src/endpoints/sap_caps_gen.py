'''
sap_caps_gen endpoints
'''
import decimal
import datetime
import json
import logging
import glob
import os
import pandas as pd
import random
import re
import zipfile
import requests
import sqlalchemy
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import *
from sqlalchemy import create_engine, MetaData
from config import *

sap_caps_gen = Blueprint('sap_caps_gen', __name__)

@sap_caps_gen.route('/unzipping', methods=['POST'])
def unzipping():
    """
    This is a function that iterates through each folder in the directory, and recursively walks to the nth level of the folder, retrieving any zipped files.
    Example Payload: {"client" : "Repsol" ,"project": "Repsol-2019", "system" : "SAP", "file" : "sanic.png", "debug" : True}
    """
    def get_cwd(read_path):
        current_directory = os.path.dirname(os.path.abspath('__file__'))
        current_file_path = os.path.join(current_directory, read_path)
        return current_file_path

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
    # mapping = db.session.query(CDM_label, DataMapping).join(DataMapping).add_columns(CDM_label.script_labels, DataMapping.column_name, DataMapping.table_name).all()


    def mapping_serializer(label):
        return {
            "script_label": label.script_labels,
            "mappings": [{"column_name": map.column_name, "table_name" : map.table_name} for map in label.cdm_label_data_mappings.all()]
        }
    mapping = [mapping_serializer(label) for label in CDM_label.query.all()]
    print(list(set([table['mappings'][0]['table_name'] for table in mapping])))
    return 'OK'
    #todo: return a list of SAP tablenames

    # response = {'status': '', 'message': {}, 'payload': []}
    # #TODO: for table names in a column (distinctify first) + find all table names and retrieve their records
    # list_of_files = []
    # for table in List_tablenames:
    #     basetable = pd.DataFrame()
    #     for file in os.listdir('caps_gen_processing/caps_gen_unzipped'):
    #         if re.search(table, file):
    #             if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
    #                 list_of_files.append[file]
    #     #Reading Data
    #     with open('{}_MASTER.txt'.format(table), 'wb') as wfd:
    #         for f in listoffiles:
    #             with open(f, 'rb') as fd:
    #                 try:
    #                     shutil.copyfileobj(fd, wfd)
    #                 except Exception as e:
    #                     response['message'].update('Unable to conatenate files for file {file} in table {table}'.format(file=f, table=table))
    #                     return response
    #         first_line = wfd.readline().rstrip().split(',')
    #         try:
    #             #todo: dictionary map to rename columns
    #             for key in dictionary.keys()
    #                 renamed_lines = [first_line.replace(key, dictionary[key]) for column in first_line]
    #
    #         except Exception as e:
    #             response['message'].update('Unable to rename columns for master table {}').format(table)
    #
    #
    #
    #
    #
    #                 basetable = pd.concat([basetable, df])
    #                 response['message'].update({'Table Upload successful' : table})
    #                 print('Table Upload Successful {}'.format(table))
    #         if len(basetable) == 0:
    #             response['status'] = 'Not OK'
    #             response['message'].update({'Missing Table' : table})
    #     uniondict[table] = basetable
    #     files_present = glob.glob('{}.csv'.format(table))
    #     if not files_present:
    #         print('Writing Master Table'.format(table))
    #         basetable.to_csv('{}.csv'.format(table), index=False)
    # return response, 200


@sap_caps_gen.route('/data_quality_check', methods=['GET'])
def data_quality_check():
    response = {
        "VERSION": current_app.config['VERSION']
    }
    return jsonify(response)

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