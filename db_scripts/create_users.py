# IMPORT INITS
import os
import sys
sys.path[0]+="/.."

# FLASK APP
from src.models import *
from src import api

# INSERTS
with api.app_context():
    db.create_all()

    base_userlist = [
        {'username': 'itra', 'password': 'test', 'email': 'lh_test_user@test.test', 'initials': 'ITRA', 'first_name': 'Ozge', 'last_name': 'Uncu', 'role': 'tax_master'},

        {'username': 'wsmith', 'password': 'test', 'email': 'wsmith@test.test', 'initials': 'WS', 'first_name': 'William', 'last_name': 'Smith', 'role': 'tax_practitioner'},
        {'username': 'msmith', 'password': 'test', 'email': 'msmith@test.test', 'initials': 'MS', 'first_name': 'Morty', 'last_name': 'Smith', 'role': 'tax_practitioner'},
        {'username': 'radams', 'password': 'test', 'email': 'radams@test.test', 'initials': 'RA', 'first_name': 'Ryan', 'last_name': 'Adams', 'role': 'tax_practitioner'},
        {'username': 'mgarcia', 'password': 'test', 'email': 'mgarcia@test.test', 'initials': 'MG', 'first_name': 'Maria', 'last_name': 'Garcia', 'role': 'tax_approver'},
        {'username': 'aochoa', 'password': 'test', 'email': 'aochoa@test.test', 'initials': 'AO', 'first_name': 'Andrea', 'last_name': 'Ochoa', 'role': 'tax_approver'},
        {'username': 'rpatel', 'password': 'test', 'email': 'rpatel@test.test', 'initials': 'RP', 'first_name': 'Russell', 'last_name': 'Patel', 'role': 'tax_approver'},
        {'username': 'creily', 'password': 'test', 'email': 'creily@test.test', 'initials': 'CR', 'first_name': 'Chris', 'last_name': 'Reily', 'role': 'tax_master'},
        {'username': 'lxiang', 'password': 'test', 'email': 'lxiang@test.test', 'initials': 'LX', 'first_name': 'Lisa', 'last_name': 'Xiang', 'role': 'tax_master'},
        {'username': 'fghosh', 'password': 'test', 'email': 'fghosh@test.test', 'initials': 'FG', 'first_name': 'Frank', 'last_name': 'Ghosh', 'role': 'tax_master'},
        {'username': 'jzafar', 'password': 'test', 'email': 'jzafar@test.test', 'initials': 'JZ', 'first_name': 'Jasmine', 'last_name': 'Zafar', 'role': 'data_master'},
        {'username': 'ddeguzman', 'password': 'test', 'email': 'ddeguzman@test.test', 'initials': 'DDG', 'first_name': 'David', 'last_name': 'DeGuzman', 'role': 'data_master'},
        {'username': 'kvaldo', 'password': 'test', 'email': 'kvaldo@test.test', 'initials': 'KV', 'first_name': 'Kiara', 'last_name': 'Valdo', 'role': 'data_master'},
        {'username': 'rsanchez', 'password': 'test', 'email': 'rsanchez@test.test', 'initials': 'RS', 'first_name': 'Rick', 'last_name': 'Sanchez', 'role': 'administrative_assistant'},
        {'username': 'psylvester', 'password': 'test', 'email': 'psylvester@test.test', 'initials': 'PS', 'first_name': 'Pen', 'last_name': 'Sylvester', 'role': 'administrative_assistant'},
        {'username': 'arails', 'password': 'test', 'email': 'arails@test.test', 'initials': 'AR', 'first_name': 'Adam', 'last_name': 'Rails', 'role': 'administrative_assistant'},
        {'username': 'vmaximus', 'password': 'test', 'email': 'vmaximus@test.test', 'initials': 'VM', 'first_name': 'Vance', 'last_name': 'Maximus', 'role': 'tax_practitioner'},

        # UAT USERS
        {'username': 'tax_master', 'password': 'test', 'email': 'tax_master@test.test', 'initials': 'tm', 'first_name': 'Tax', 'last_name': 'Master', 'role': 'tax_master'},
        {'username': 'data_master', 'password': 'test', 'email': 'data_master@test.test', 'initials': 'dm', 'first_name': 'Data', 'last_name': 'Master', 'role': 'data_master'},

    ]

    for data in base_userlist:
        newuser = User(
            username = data['username'],
            password = User.generate_hash(data['password']),
            email = data['email'],
            initials = data['initials'].upper(),
            first_name = data['first_name'],
            last_name = data['last_name'],
            role = data['role']
        )
        db.session.add(newuser)

    # LH GVA USER
    db.session.add(User(
        username = 'lh-admin', password = User.generate_hash('Kpmg1234%'),
        email = 'ca-fmgvalhrhadmin@kpmg.ca',
        initials = 'lh'.upper(), first_name = 'Lighthouse', last_name = 'GVA',
        role = 'tax_master', is_system_administrator = True, is_superuser = True
    ))

    # LH GVA USER


    # ITRA USERS
    itra_userlist = [
        {'username': 'ejensen', 'password': 'ejensen', 'email': 'ejensen@test.test', 'initials': 'edj', 'first_name': 'Erin', 'last_name': 'Jensen', 'role': 'tax_master'},
        {'username': 'nataliakrizbai', 'password': 'nataliakrizbai', 'email': 'nataliakrizbai@test.test', 'initials': 'nk', 'first_name': 'Natalia', 'last_name': 'Krizbai', 'role': 'tax_master'},
        {'username': 'dcallow', 'password': 'dcallow', 'email': 'dcallow@test.test', 'initials': 'dtc', 'first_name': 'Dylan', 'last_name': 'Callow', 'role': 'tax_master'},
        {'username': 'ryansen', 'password': 'ryansen', 'email': 'ryansen@test.test', 'initials': 'rjs', 'first_name': 'Ryan', 'last_name': 'Sen', 'role': 'tax_master'},
        {'username': 'karinadewi', 'password': 'karinadewi', 'email': 'karinadewi@test.test', 'initials': 'kd', 'first_name': 'Karina', 'last_name': 'Dewi', 'role': 'tax_master'},
        {'username': 'jasonclee', 'password': 'jasonclee', 'email': 'jasonclee@test.test', 'initials': 'jcl', 'first_name': 'Jason', 'last_name': 'Lee', 'role': 'tax_master'},
        {'username': 'andylee1', 'password': 'andylee1', 'email': 'andylee1@test.test', 'initials': 'al', 'first_name': 'Andy', 'last_name': 'Lee', 'role': 'tax_master'},
    ]
    for data in itra_userlist:
        newuser = User(
            username = data['username'],
            password = User.generate_hash(data['password']),
            email = data['email'],
            initials = data['initials'].upper(),
            first_name = data['first_name'],
            last_name = data['last_name'],
            role = data['role'],
            is_system_administrator = True
        )
        db.session.add(newuser)

    # COMMIT CHANGES
    db.session.commit()
