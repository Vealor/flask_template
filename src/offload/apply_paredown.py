
import os
import re
import json
import requests
import multiprocessing as mp
from config import *
from flask import Blueprint, current_app, jsonify, request
from os import path
from sqlalchemy import exists, desc, create_engine
from src.models import *
from src.errors import *

#===============================================================================
def apply_rules_to_txn(args):
    tempsession = db.create_scoped_session()
    rules = args['rules']
    txn = tempsession.query(Transaction).filter_by(id=args['txn_id']).first()
    print(txn.id)
    for rule in rules:
        # variable for checking conditions
        do_paredown = 0
        for condition in rule['conditions']:
            # print(condition)
            # ensure the field for the condition is in the data keys
            if condition['field'] in txn.data:

                if condition['operator'] == 'contains':
                    # print("\tCONTAINS")
                    if re.search('(?<!\S)'+condition['value'].lower()+'(?!\S)', txn.data[condition['field']].lower()):
                        do_paredown +=1

                elif condition['operator'] in ['>','<','==','>=','<=','!=']:
                    # print("\tLOGICAL OPERATOR")
                    proceed_operator = True

                    try:
                        value = float(condition['value'])
                        field = float(txn.data[condition['field']])
                    except ValueError as e:
                        # failed +=1
                        proceed_operator = False

                    if proceed_operator:
                        if condition['operator'] == '>' and value > field:
                            do_paredown +=1
                        elif condition['operator'] == '<' and value < field:
                            do_paredown +=1
                        elif condition['operator'] == '==' and value == field:
                            do_paredown +=1
                        elif condition['operator'] == '>=' and value >= field:
                            do_paredown +=1
                        elif condition['operator'] == '<=' and value <= field:
                            do_paredown +=1
                        elif condition['operator'] == '!=' and value != field:
                            do_paredown +=1
                    else:
                        print("Condition value or Transaction data field not fit for operator comparison.")
                else:
                    raise Exception("Database issue for ParedownRuleCondition operator.")

        # if all conditions succeeded
        if do_paredown == len(rule['conditions']):
            # print("APPLY PAREDOWN TO TXN")
            if not txn.gst_signed_off_by_id:
                txn.update_gst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.gst_codes] if txn.gst_codes else []),tempsession)
            if not txn.hst_signed_off_by_id:
                txn.update_hst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.hst_codes] if txn.hst_codes else []),tempsession)
            if not txn.qst_signed_off_by_id:
                txn.update_qst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.qst_codes] if txn.qst_codes else []),tempsession)
            if not txn.pst_signed_off_by_id:
                txn.update_pst_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.pst_codes] if txn.pst_codes else []),tempsession)
            if not txn.apo_signed_off_by_id:
                txn.update_apo_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.apo_codes] if txn.apo_codes else []),tempsession)

    tempsession.commit()
