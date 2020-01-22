import json
import os
import sys
sys.path.append(sys.path[0] + "/..")

# FLASK APP
from src.core.models import db, CDMLabel, User  # noqa: E402
from src.itra.models import Code, ParedownRule, ParedownRuleCondition  # noqa: E402
from src import api  # noqa: E402

# ==============================================================================
def seed_cdm_labels(data):
    print('\n\033[34mSEED CDM Labels\033[0m\n')
    with api.app_context():
        try:
            for entry in data:
                new_label = CDMLabel(
                    caps_interface = entry['caps_interface'],
                    category = entry['category'],
                    datatype = entry['datatype'],
                    display_name = entry['display_name'],
                    is_calculated = entry['is_calculated'],
                    is_unique = entry['is_unique'],
                    length = entry['length'],
                    script_label = entry['script_label']
                )
                if 'is_active' in entry.keys():
                    new_label.is_active = True
                if 'precision' in entry.keys():
                    new_label.precision = int(entry['precision'])
                db.session.add(new_label)
            db.session.commit()
        except Exception as e:
            print('\n\t\033[31mERROR\033[0m => cdm_labels\n')
            print(e)
            db.session.rollback()

def seed_codes(data):
    print('\n\033[34mSEED Codes\033[0m\n')
    with api.app_context():
        try:
            for entry in data:
                new_code = Code(
                    code_number = entry['code_number'],
                    description = entry['description']
                )
                db.session.add(new_code)
            db.session.commit()
        except Exception as e:
            print('\n\t\033[31mERROR\033[0m => codes\n')
            print(e)
            db.session.rollback()

def seed_paredown_rules(data):
    print('\n\033[34mSEED Paredown Rules\033[0m\n')
    with api.app_context():
        try:
            for entry in data:
                code_id = (Code.query.filter_by(code_number = entry['paredown_rule_code']).first()).serialize['id']
                new_paredown_rule = ParedownRule(
                    code_id = int(code_id),
                    is_core = entry['is_core']
                )
                if 'comment' in entry.keys():
                    new_paredown_rule.comment = entry['comment']
                db.session.add(new_paredown_rule)
                db.session.flush()
                for condition in entry['conditions']:
                    new_paredown_rule_condition = ParedownRuleCondition(
                        field = condition['field'],
                        value = condition['value'],
                        operator = condition['operator'],
                        paredown_rule_id = new_paredown_rule.id
                    )
                    db.session.add(new_paredown_rule_condition)
            db.session.commit()
        except Exception as e:
            print('\n\t\033[31mERROR\033[0m => paredown_rules\n')
            print(e)
            db.session.rollback()

def seed_users(data):
    print('\n\033[34mSEED Users\033[0m\n')
    with api.app_context():
        try:
            for entry in data:
                new_user = User(
                    email = entry['email'],
                    first_name = entry['first_name'],
                    last_name = entry['last_name'],
                    username = entry['username'],
                    password = User.generate_hash(entry['password']),
                    initials = entry['initials'],
                    role = entry['role']
                )
                if 'is_system_administrator' in entry.keys():
                    new_user.is_system_administrator = True
                if 'is_superuser' in entry.keys():
                    new_user.is_superuser = True
                db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print('\n\t\033[31mERROR\033[0m => users\n')
            print(e)
            db.session.rollback()


# ==============================================================================
# perform seeding
def do_seed():
    # set active path of this file
    curr_path = os.path.dirname(os.path.realpath(__file__)) + '/'

    # base seed files to be done
    # NOTE: CODES MUST COME BEFORE PAREDOWN_RULES
    seed_files = [
        'cdm_labels.json',
        'codes.json',
        'paredown_rules.json',
        'users.json'
    ]
    for file in seed_files:
        with open(curr_path + file, 'r') as json_file:
            data = json.load(json_file)  # noqa: F841
            eval('seed_' + file.split('.')[0] + '(data)')

# ==============================================================================
if __name__ == "__main__":
    do_seed()
