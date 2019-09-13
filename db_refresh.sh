# if new migrations are required:
#
# source activate
# FLASK_ENV='development' flask db migrate

sudo -i -u postgres psql <<EOF
drop database itra_db;
create database itra_db;
grant all privileges on database itra_db to itra;
EOF
source activate
FLASK_ENV='development' flask db upgrade

read -n 1 -s -r -p "DB Entry Next >> Press any key to continue" && printf "\n"

psql -h localhost -U itra itra_db -c "
  insert into users (role, username, password, email, initials, first_name, last_name, is_superuser)
    values ('tax_master', 'test', 'test', 'lh_test_user@kpmg.ca', 'TEST', 'test_first', 'test_last', 't');
  insert into logs (action, affected_entity, details, user_id) values('create', 'everything', 'such detail', 1);

  insert into clients (name) values ('mining corp');
  insert into clients (name) values ('mining corp two');
  insert into clients (name) values ('mining corpses');
  insert into client_entities (client_id, company_code, lob_sector) values (1, '78GK', 'consumer_retail_food_beverage');
  insert into client_entity_jurisdictions (client_entity_id, jurisdiction) values (1, 'bc');
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 49er', 1, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 49er two', 1, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 50er', 2, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 51er', 3, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values (E'I\'m a lumberjack and I\'m okay', 3, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('trees bro', 3, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('fish n oceans n shit', 3, 1, 1);
  insert into vendors (name) values ('miner buyer');
  insert into transactions (data, vendor_id, project_id) values ('{}', 1, 1);
  insert into user_project (user_id, project_id) values (1, 1);

  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_practitioner', 'pepperpotts', 'test', 'pepperpotts@test.test', 'pp', 'pepper', 'potts');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_practitioner', 'antman', 'test', 'antman@test.test', 'am', 'ant', 'man');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_practitioner', 'spiderman', 'test', 'spiderman@test.test', 'sm', 'spider', 'man');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_approver', 'ironman', 'test', 'ironman@test.test', 'im', 'iron', 'man');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_approver', 'blackpanther', 'test', 'blackpanther@test.test', 'bp', 'black', 'panther');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_approver', 'deadpool', 'test', 'deadpool@test.test', 'dp', 'dead', 'pool');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_master', 'captainamerica', 'test', 'captainamerica@test.test', 'ca', 'captain', 'america');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_master', 'captainmarvel', 'test', 'captainmarvel@test.test', 'cm', 'captain', 'marvel');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('tax_master', 'lukecage', 'test', 'lukecage@test.test', 'lc', 'luke', 'cage');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('data_master', 'incrediblehulk', 'test', 'incrediblehulk@test.test', 'ih', 'incredible', 'hulk');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('data_master', 'doctorstrange', 'test', 'doctorstrange@test.test', 'drs', 'doctor', 'strange');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('data_master', 'hawkeye', 'test', 'hawkeye@test.test', 'hwk', 'hawk', 'eye');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('administrative_assistant', 'blackwidow', 'test', 'blackwidow@test.test', 'bw', 'black', 'widow');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('administrative_assistant', 'edwinjarvis', 'test', 'edwinjarvis@test.test', 'ej', 'edwin', 'jarvis');
  insert into users (role, username, password, email, initials, first_name, last_name)
    values ('administrative_assistant', 'philcoulson', 'test', 'philcoulson@test.test', 'pc', 'phil', 'coulson');
  insert into users (role, username, password, email, initials, first_name, last_name, is_system_administrator)
    values ('tax_practitioner', 'nickfury', 'test', 'nickfury@test.test', 'nf', 'nick', 'fury', 't');

  insert into user_project (user_id, project_id) values (2, 1);
  insert into user_project (user_id, project_id) values (3, 2);
  insert into user_project (user_id, project_id) values (3, 3);
  insert into user_project (user_id, project_id) values (4, 4);
  insert into user_project (user_id, project_id) values (4, 5);
  insert into user_project (user_id, project_id) values (4, 6);
  insert into user_project (user_id, project_id) values (5, 7);
  insert into user_project (user_id, project_id) values (6, 1);
  insert into user_project (user_id, project_id) values (7, 2);
  insert into user_project (user_id, project_id) values (8, 3);
  insert into user_project (user_id, project_id) values (8, 4);
  insert into user_project (user_id, project_id) values (8, 5);
  insert into user_project (user_id, project_id) values (9, 6);
  insert into user_project (user_id, project_id) values (10, 7);
  insert into user_project (user_id, project_id) values (10, 1);
  insert into user_project (user_id, project_id) values (11, 2);
  insert into user_project (user_id, project_id) values (11, 3);
  insert into user_project (user_id, project_id) values (11, 4);
  insert into user_project (user_id, project_id) values (12, 5);
  insert into user_project (user_id, project_id) values (13, 6);
  insert into user_project (user_id, project_id) values (13, 7);
  insert into user_project (user_id, project_id) values (14, 1);
  insert into user_project (user_id, project_id) values (14, 2);
  insert into user_project (user_id, project_id) values (14, 3);
  insert into user_project (user_id, project_id) values (15, 4);
  insert into user_project (user_id, project_id) values (16, 5);
  insert into user_project (user_id, project_id) values (16, 6);
  insert into user_project (user_id, project_id) values (17, 7);
  insert into user_project (user_id, project_id) values (17, 1);
  insert into user_project (user_id, project_id) values (17, 2);
  "


##
