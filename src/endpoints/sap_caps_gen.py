'''
sap_caps_gen endpoints
'''
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
from azure.storage.file import FileService
from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from src.models import DataMapping, db
from sqlalchemy import create_engine, MetaData
from config import *

sap_caps_gen = Blueprint('sap_caps_gen', __name__)
file_service = FileService(account_name='itrauat', account_key='ln5Ioy8hJGzokewjo+9Wu5XlQtWhfGqTT5jw66sF+nLgpLsA+mnsSaxwaBDDkRTfEFtXxNU1MgfMu2I3AlsV6Q==')

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
        file_service.get_file_to_path('itra', '{project}/{system}_data'.format(project=data['project'], system=data['system']), '{file}'.format(file=data['file']), 'caps_gen_processing/caps_gen_raw/{file}'.format(file=data['file']))

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
    response = {'status': '', 'message': {}, 'payload': []}
    #TODO: for table names in a column (distinctify first) + find all table names and retrieve their records
    tables = ['AUFK', 'BKPF', 'BSAK', 'BSEG', 'CEPCT', 'CSKS', 'CSKT', 'EKKO', 'EKPO', 'IFLOT', 'ILOA', 'LFA1', 'MAKT',
             'MARA', 'PAYR', 'PROJ', 'PRPS', 'REGUP', 'SKAT', 'T001W', 'T007S']
    uniondict = {}
    for table in tables:
        basetable = pd.DataFrame()
        for file in os.listdir('caps_gen_processing/caps_gen_unzipped'):
            if re.search(table, file):
                if re.match(("^((?<!_[A-Z]{4}).)*" + re.escape(table) + "_\d{4}"), file):
                    #Reading Data
                    df = pd.read_csv(os.path.join('caps_gen_processing/caps_gen_unzipped', file), delimiter='\#\|\#',
                                     dtype=str,  # dtypedict,
                                     # parse_dates=parse_dates,
                                     # date_parser= pd.to_datetime,
                                      error_bad_lines=True,
                                      warn_bad_lines=True,
                                     engine='python')
                    #Renaming Data Columns
                    df.columns = df.columns.str.replace(r'[^a-zA-Z0-9_-]', '')
                    rename_dict = {}
                    # renaming process
                    for i in df.columns.values:
                        for j in jsondata['mapping']:
                            for g in jsondata['mapping'][j]['association'].keys():
                                if re.search('({})_'.format(table), g):  # search for BSEG in filename
                                    if jsondata['mapping'][j]['association'][g] == i:
                                        print('table: ' + str(table) + str(i) + ' will be mapped to ' + str(j))
                                        rename_dict[i] = j
                                        try:
                                            dtypedict[j] = dtypedict.pop(i)
                                        except:
                                            print('datatypes have already been converted in the first file')
                    #
                    basetable = pd.concat([basetable, df])
                    response['message'].update({'Table Upload successful' : table})
                    print('Table Upload Successful {}'.format(table))
            if len(basetable) == 0:
                response['status'] = 'Not OK'
                response['message'].update({'Missing Table' : table})
        uniondict[table] = basetable
        files_present = glob.glob('{}.csv'.format(table))
        if not files_present:
            print('Writing Master Table'.format(table))
            basetable.to_csv('{}.csv'.format(table), index=False)
    return response, 200


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