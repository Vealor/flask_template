'''
sap_caps_gen endpoints
'''
import json
import logging
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

playground = Blueprint('playground', __name__)

@playground.route('/generate_data', methods=['GET'])
def generate_data():
    response = {'status': '', 'message': {}, 'payload': []}
    engine = create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    db_conn = engine.connect()
    metadata = MetaData(engine, reflect=True)
    metadata.create_all()
    df = pd.read_csv('CDM_Temp.csv')
    df = df.loc[df['origin'] == 'CDM']
    json_entries = df.to_json(orient='records',lines=True).split('\n')
    CDM_table = metadata.tables['data_mappings']
    for entry in json_entries:
        stmt = CDM_table.insert(json.loads(entry))
        db_conn.execute(stmt)
    return "Process Completed"