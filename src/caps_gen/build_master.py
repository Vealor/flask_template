
import os
import re
import json
import requests
import multiprocessing as mp
from config import *
from flask import Blueprint, current_app, jsonify, request
from os import path
from src.models import *
from sqlalchemy import exists, desc, create_engine
from sqlalchemy.sql.expression import bindparam

def build_master_file(args):
    table = args['table']
    data = args['data']
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

def build_master_table(args):
    table = args['table']
    data = args['data']
    caps_gen_id = args['id']
    print('starting insert' + str(table))
    #initialize variables for bulk insertion
    referenceclass = eval('Sap' + str(table.lower().capitalize()))
    list_to_insert = []
    engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))

    counter = 0
    #bulk insert into database
    with open(os.path.join(current_app.config['CAPS_BASE_DIR'], str(data['project_id']), 'caps_gen_master', '{}_MASTER.txt'.format(table)), 'r', encoding='utf-8-sig') as masterfile:
        header = masterfile.readline()
        header = header.rstrip('\n').split('#|#')
        for line in masterfile:
            # insert rows chunk by chunk to avoid crashing
            #  NOTE: 200,000 entries use about 4GB ram
            if counter >= 200000:
                engine.execute(referenceclass.__table__.insert(), list_to_insert)
                counter = 0
                list_to_insert = []
            else:
                counter += 1
                list_to_insert.append({"caps_gen_id": caps_gen_id, 'data': dict(zip(header, line.rstrip('\n').split('#|#')))})
        if counter > 0:
            engine.execute(referenceclass.__table__.insert(), list_to_insert)
    print('complete insert' + str(table))

def apply_mapping(args):

    table = args['table']
    print("start:{}".format(table))
    table_name = args['table'].lower().partition('sap')[2]
    label = args['label']
    id = args['id']
    limit = 100000
    offset = 0
    referenceclass = eval(table)
    engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%'))
    # print(table)
    def map_data(limit, offset):
        query_string = '''
        SELECT * from sap_{table} WHERE caps_gen_id={id} ORDER BY id LIMIT {limit} OFFSET {offset};
        '''.format(table = table_name, limit = limit, offset = offset, id = id )

        result = engine.execute(query_string)
        stmt = referenceclass.__table__.update().\
                where(referenceclass.id == bindparam('_id')).\
                values({
                    'data': bindparam('data'),
                    'caps_gen_id': bindparam('caps_gen_id'),
                })

        columns = [i for i in result]
        list_to_inset = []
        for row in columns:
            newdata = dict(row.data)
            if not row.data:
                print("data empty")
            # print(row.data)
            for map in label:
                if map[0] in newdata.keys():
                    newdata[map[1]] = newdata.pop(map[0])
                # print("yay")
                # row.data = newdata
            insert_data = {'_id':row.id, 'data':newdata, 'caps_gen_id':id}
            list_to_inset.append(insert_data)

        # print('insert')
        # print(list_to_inset)
        if len(list_to_inset)>0:
            engine.execute(stmt, list_to_inset)
        # db.session.commit()
        return len(columns)
    qlen = 1
    while qlen > 0:
        qlen = map_data(limit, offset)
        offset += limit
    print("complete:{}".format(table))
