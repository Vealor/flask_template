
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
                        if condition['operator'] == '>' and field > value:
                            do_paredown +=1
                        elif condition['operator'] == '<' and field < value:
                            do_paredown +=1
                        elif condition['operator'] == '==' and field == value:
                            do_paredown +=1
                        elif condition['operator'] == '>=' and field >= value:
                            do_paredown +=1
                        elif condition['operator'] == '<=' and field <= value:
                            do_paredown +=1
                        elif condition['operator'] == '!=' and field != value:
                            do_paredown +=1
                    else:
                        print("Condition value or Transaction data field not fit for operator comparison.")
                else:
                    raise Exception("Database issue for ParedownRuleCondition operator.")

        # if all conditions succeeded
        if do_paredown == len(rule['conditions']):
            # print("APPLY PAREDOWN TO TXN")
            if not txn.gst_signed_off_by_id:
                txn.update_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'gst'] if txn.transaction_codes else []), 'gst', tempsession)
            if not txn.hst_signed_off_by_id:
                txn.update_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'hst'] if txn.transaction_codes else []), 'hst', tempsession)
            if not txn.qst_signed_off_by_id:
                txn.update_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'qst'] if txn.transaction_codes else []), 'qst', tempsession)
            if not txn.pst_signed_off_by_id:
                txn.update_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'pst'] if txn.transaction_codes else []), 'pst', tempsession)
            if not txn.apo_signed_off_by_id:
                txn.update_codes([rule['code']['code_number']] + ([c.serialize['code'] for c in txn.transaction_codes if c.tax_type.value == 'apo'] if txn.transaction_codes else []), 'apo', tempsession)

    tempsession.commit()
