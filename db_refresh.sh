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

read -n 1 -s -r -p "START SERVER NOW >> Press any key to continue once started" && printf "\n"

function make_user () {
  curl -H "Content-Type: application/json" -X POST -d '{
    "username":"'$1'",
    "password":"'$2'",
    "email":"'$3'",
    "initials":"'$4'",
    "first_name":"'$5'",
    "last_name":"'$6'",
    "role":"'$7'"
  }' http://localhost:5000/users
}
make_user "test" "test" "lh_test_user@test.test" "TEST" "test_first" "test_last" "tax_master"

make_user "pepperpotts" "test" "pepperpotts@test.test" "pp" "pepper" "potts" "tax_practitioner"
make_user "antman" "test" "antman@test.test" "am" "ant" "man" "tax_practitioner"
make_user "spiderman" "test" "spiderman@test.test" "sm" "spider" "man" "tax_practitioner"
make_user "ironman" "test" "ironman@test.test" "im" "iron" "man" "tax_approver"
make_user "blackpanther" "test" "blackpanther@test.test" "bp" "black" "panther" "tax_approver"
make_user "deadpool" "test" "deadpool@test.test" "dp" "dead" "pool" "tax_approver"
make_user "captainamerica" "test" "captainamerica@test.test" "ca" "captain" "america" "tax_master"
make_user "captainmarvel" "test" "captainmarvel@test.test" "cm" "captain" "marvel" "tax_master"
make_user "lukecage" "test" "lukecage@test.test" "lc" "luke" "cage" "tax_master"
make_user "incrediblehulk" "test" "incrediblehulk@test.test" "ih" "incredible" "hulk" "data_master"
make_user "doctorstrange" "test" "doctorstrange@test.test" "drs" "doctor" "strange" "data_master"
make_user "hawkeye" "test" "hawkeye@test.test" "hwk" "hawk" "eye" "data_master"
make_user "blackwidow" "test" "blackwidow@test.test" "bw" "black" "widow" "administrative_assistant"
make_user "edwinjarvis" "test" "edwinjarvis@test.test" "ej" "edwin" "jarvis" "administrative_assistant"
make_user "philcoulson" "test" "philcoulson@test.test" "pc" "phil" "coulson" "administrative_assistant"
make_user "nickfury" "test" "nickfury@test.test" "nf" "nick" "fury" "tax_practitioner"

psql -h localhost -U itra itra_db -c "
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

  update users set req_pass_reset = 'f';
  update users set is_superuser = 'y' where id = 1;
  update users set is_system_administrator = 'y' where id = 17;

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


  insert into paredown_rules (id, code) values (1, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (1, 'Acct_Desc', 'contains', 'Donation');

  insert into paredown_rules (id, code) values (2, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (2, 'Item_Text', 'contains', 'Donation');

  insert into paredown_rules (id, code) values (3, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (3, 'INVOICE_NUM', 'contains', 'Donation');

  insert into paredown_rules (id, code) values (4, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (4, 'Acct_Desc', 'contains', 'Sponsorship');

  insert into paredown_rules (id, code) values (5, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (5, 'Item_Text', 'contains', 'Sponsorship');

  insert into paredown_rules (id, code) values (6, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (6, 'INVOICE_NUM', 'contains', 'Sponsorship');

  insert into paredown_rules (id, code) values (7, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (7, 'Acct_Desc', 'contains', 'Charity');

  insert into paredown_rules (id, code) values (8, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (8, 'Item_Text', 'contains', 'Charity');

  insert into paredown_rules (id, code) values (9, '210');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (9, 'INVOICE_NUM', 'contains', 'Charity');

  insert into paredown_rules (id, code, comment) values (10, '221', 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (10, 'Acct_Desc', 'contains', 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (10, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (11, '221', 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (11, 'Item_Text', 'contains', 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (11, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (12, '221', 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (12, 'INVOICE_NUM', 'contains', 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (12, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (13, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (13, 'Acct_Desc', 'contains', 'Health');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (13, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (14, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (14, 'Item_Text', 'contains', 'Health');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (14, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (15, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (15, 'INVOICE_NUM', 'contains', 'Health');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (15, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (16, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (16, 'Acct_Desc', 'contains', 'Dental');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (16, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (17, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (17, 'Item_Text', 'contains', 'Dental');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (17, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (18, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (18, 'INVOICE_NUM', 'contains', 'Dental');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (18, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (19, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (19, 'Acct_Desc', 'contains', 'Disability');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (19, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (20, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (20, 'Item_Text', 'contains', 'Disability');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (20, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (21, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (21, 'INVOICE_NUM', 'contains', 'Disability');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (21, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (22, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (22, 'Acct_Desc', 'contains', 'LTD');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (22, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (23, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (23, 'Item_Text', 'contains', 'LTD');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (23, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (24, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (24, 'INVOICE_NUM', 'contains', 'LTD');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (24, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (25, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (25, 'Acct_Desc', 'contains', 'STD');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (25, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (26, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (26, 'Item_Text', 'contains', 'STD');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (26, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (27, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (27, 'INVOICE_NUM', 'contains', 'STD');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (27, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (28, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (28, 'Acct_Desc', 'contains', 'Medical');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (28, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (29, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (29, 'Item_Text', 'contains', 'Medical');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (29, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (30, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (30, 'INVOICE_NUM', 'contains', 'Medical');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (30, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (31, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (31, 'Acct_Desc', 'contains', 'Medical Services Plan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (31, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (32, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (32, 'Item_Text', 'contains', 'Medical Services Plan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (32, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (33, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (33, 'Acct_Desc', 'contains', 'MSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (33, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (34, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (34, 'Item_Text', 'contains', 'MSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (34, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (35, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (35, 'INVOICE_NUM', 'contains', 'MSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (35, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (36, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (36, 'Acct_Desc', 'contains', 'Payroll');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (36, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (37, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (37, 'Item_Text', 'contains', 'Payroll');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (37, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (38, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (38, 'INVOICE_NUM', 'contains', 'Payroll');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (38, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (39, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (39, 'Acct_Desc', 'contains', 'Salary');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (39, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (40, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (40, 'Item_Text', 'contains', 'Salary');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (40, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (41, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (41, 'INVOICE_NUM', 'contains', 'Salary');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (41, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (42, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (42, 'Acct_Desc', 'contains', 'Salaries');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (42, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (43, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (43, 'Item_Text', 'contains', 'Salaries');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (43, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (44, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (44, 'INVOICE_NUM', 'contains', 'Salaries');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (44, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (45, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (45, 'Acct_Desc', 'contains', 'Severance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (45, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (46, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (46, 'Item_Text', 'contains', 'Severance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (46, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (47, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (47, 'INVOICE_NUM', 'contains', 'Severance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (47, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (48, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (48, 'Acct_Desc', 'contains', 'Employment insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (48, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (49, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (49, 'Item_Text', 'contains', 'Employment insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (49, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (50, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (50, 'Acct_Desc', 'contains', 'Employer Health Tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (50, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (51, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (51, 'Item_Text', 'contains', 'Employer Health Tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (51, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (52, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (52, 'Acct_Desc', 'contains', 'EHT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (52, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (53, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (53, 'Item_Text', 'contains', 'EHT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (53, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (54, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (54, 'INVOICE_NUM', 'contains', 'EHT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (54, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (55, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (55, 'Acct_Desc', 'contains', 'Garnish');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (55, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (56, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (56, 'Item_Text', 'contains', 'Garnish');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (56, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (57, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (57, 'INVOICE_NUM', 'contains', 'Garnish');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (57, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (58, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (58, 'Acct_Desc', 'contains', 'Share purchase');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (58, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (59, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (59, 'Item_Text', 'contains', 'Share purchase');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (59, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (60, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (60, 'Acct_Desc', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (60, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (61, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (61, 'Item_Text', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (61, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (62, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (62, 'INVOICE_NUM', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (62, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (63, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (63, 'Acct_Desc', 'contains', 'RRSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (63, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (64, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (64, 'Item_Text', 'contains', 'RRSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (64, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (65, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (65, 'INVOICE_NUM', 'contains', 'RRSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (65, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (66, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (66, 'Acct_Desc', 'contains', 'Work Safety');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (66, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (67, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (67, 'Item_Text', 'contains', 'Work Safety');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (67, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (68, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (68, 'Acct_Desc', 'contains', 'Workers Comp');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (68, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (69, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (69, 'Item_Text', 'contains', 'Workers Comp');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (69, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (70, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (70, 'Acct_Desc', 'contains', 'workers compensation board');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (70, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (71, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (71, 'Item_Text', 'contains', 'workers compensation board');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (71, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (72, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (72, 'Acct_Desc', 'contains', 'Worksafe BC');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (72, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (73, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (73, 'Item_Text', 'contains', 'Worksafe BC');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (73, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (74, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (74, 'Acct_Desc', 'contains', 'WorksafeBC');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (74, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (75, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (75, 'Item_Text', 'contains', 'WorksafeBC');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (75, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (76, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (76, 'Acct_Desc', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (76, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (77, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (77, 'Item_Text', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (77, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (78, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (78, 'INVOICE_NUM', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (78, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (79, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (79, 'Acct_Desc', 'contains', 'WSIB');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (79, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (80, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (80, 'Item_Text', 'contains', 'WSIB');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (80, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (81, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (81, 'INVOICE_NUM', 'contains', 'WSIB');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (81, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (82, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (82, 'Acct_Desc', 'contains', 'Workplace Safety & Insurance Board');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (82, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (83, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (83, 'Item_Text', 'contains', 'Workplace Safety & Insurance Board');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (83, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (84, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (84, 'Acct_Desc', 'contains', 'Canada Pension Plan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (84, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (85, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (85, 'Item_Text', 'contains', 'Canada Pension Plan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (85, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (86, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (86, 'Acct_Desc', 'contains', 'WCB');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (86, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (87, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (87, 'Item_Text', 'contains', 'WCB');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (87, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (88, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (88, 'INVOICE_NUM', 'contains', 'WCB');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (88, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (89, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (89, 'Acct_Desc', 'contains', 'Union due');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (89, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (90, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (90, 'Item_Text', 'contains', 'Union due');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (90, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (91, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (91, 'Acct_Desc', 'contains', 'Pension');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (91, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (92, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (92, 'Item_Text', 'contains', 'Pension');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (92, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (93, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (93, 'INVOICE_NUM', 'contains', 'Pension');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (93, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (94, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (94, 'Acct_Desc', 'contains', 'Dividends');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (94, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (95, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (95, 'Item_Text', 'contains', 'Dividends');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (95, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (96, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (96, 'INVOICE_NUM', 'contains', 'Dividends');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (96, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (97, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (97, 'Acct_Desc', 'contains', 'EI ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (97, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (98, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (98, 'Item_Text', 'contains', 'EI ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (98, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (99, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (99, 'Acct_Desc', 'contains', 'CPP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (99, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (100, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (100, 'Item_Text', 'contains', 'CPP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (100, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (101, '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (101, 'INVOICE_NUM', 'contains', 'CPP');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (101, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (102, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (102, 'Acct_Desc', 'contains', 'Loan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (102, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (103, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (103, 'Item_Text', 'contains', 'Loan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (103, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (104, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (104, 'INVOICE_NUM', 'contains', 'Loan');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (104, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (105, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (105, 'Acct_Desc', 'contains', 'Debt');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (105, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (106, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (106, 'Item_Text', 'contains', 'Debt');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (106, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (107, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (107, 'INVOICE_NUM', 'contains', 'Debt');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (107, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (108, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (108, 'Acct_Desc', 'contains', 'Interest');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (108, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (109, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (109, 'Item_Text', 'contains', 'Interest');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (109, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (110, '209');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (110, 'INVOICE_NUM', 'contains', 'Interest');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (110, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (111, '221', 'Tolls');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (111, 'Acct_Desc', 'contains', 'Toll');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (111, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code, comment) values (112, '221', 'Tolls');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (112, 'Item_Text', 'contains', 'Toll');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (112, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (id, code) values (113, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (113, 'INVOICE_NUM', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (113, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (113, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (114, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (114, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (114, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (114, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (115, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (115, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (115, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (115, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (116, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (116, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (116, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (116, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (117, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (117, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (117, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (117, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (118, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (118, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (118, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (118, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (119, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (119, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (119, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (119, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (120, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (120, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (120, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (120, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (121, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (121, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (121, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (121, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (122, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (122, 'INVOICE_NUM', 'contains', 'CT ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (122, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (122, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (123, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (123, 'Acct_Desc', 'contains', 'CT ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (123, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (123, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (124, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (124, 'Item_Text', 'contains', 'CT ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (124, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (124, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (125, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (125, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (125, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (125, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (126, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (126, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (126, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (126, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (127, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (127, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (127, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (127, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (128, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (128, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (128, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (128, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (129, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (129, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (129, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (129, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (130, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (130, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (130, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (130, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (131, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (131, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (131, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (131, 'Acct_Desc', 'contains', 'tax');

  insert into paredown_rules (id, code) values (132, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (132, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (132, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (132, 'Item_Text', 'contains', 'tax');

  insert into paredown_rules (id, code) values (133, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (133, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (133, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (133, 'INVOICE_NUM', 'contains', 'MFT');

  insert into paredown_rules (id, code) values (134, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (134, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (134, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (134, 'Acct_Desc', 'contains', 'MFT');

  insert into paredown_rules (id, code) values (135, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (135, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (135, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (135, 'Item_Text', 'contains', 'MFT');

  insert into paredown_rules (id, code) values (136, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (136, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (136, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (136, 'INVOICE_NUM', 'contains', 'PST ');

  insert into paredown_rules (id, code) values (137, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (137, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (137, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (137, 'Acct_Desc', 'contains', 'PST ');

  insert into paredown_rules (id, code) values (138, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (138, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (138, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (138, 'Item_Text', 'contains', 'PST ');

  insert into paredown_rules (id, code) values (139, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (139, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (139, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (139, 'INVOICE_NUM', 'contains', 'CT ');

  insert into paredown_rules (id, code) values (140, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (140, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (140, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (140, 'Acct_Desc', 'contains', 'CT ');

  insert into paredown_rules (id, code) values (141, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (141, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (141, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (141, 'Item_Text', 'contains', 'CT ');

  insert into paredown_rules (id, code) values (142, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (142, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (142, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (142, 'INVOICE_NUM', 'contains', 'GST');

  insert into paredown_rules (id, code) values (143, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (143, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (143, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (143, 'Acct_Desc', 'contains', 'GST');

  insert into paredown_rules (id, code) values (144, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (144, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (144, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (144, 'Item_Text', 'contains', 'GST');

  insert into paredown_rules (id, code) values (145, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (145, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (145, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (145, 'INVOICE_NUM', 'contains', 'QST');

  insert into paredown_rules (id, code) values (146, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (146, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (146, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (146, 'Acct_Desc', 'contains', 'QST');

  insert into paredown_rules (id, code) values (147, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (147, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (147, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (147, 'Item_Text', 'contains', 'QST');

  insert into paredown_rules (id, code) values (148, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (148, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (148, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (148, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (149, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (149, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (149, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (149, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (150, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (150, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (150, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (150, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (151, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (151, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (151, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (151, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (152, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (152, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (152, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (152, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (153, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (153, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (153, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (153, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (154, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (154, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (154, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (154, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (155, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (155, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (155, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (155, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (156, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (156, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (156, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (156, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (157, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (157, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (157, 'INVOICE_NUM', 'contains', 'CT ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (157, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (158, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (158, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (158, 'Acct_Desc', 'contains', 'CT ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (158, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (159, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (159, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (159, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (159, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (160, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (160, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (160, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (160, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (161, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (161, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (161, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (161, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (162, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (162, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (162, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (162, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (163, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (163, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (163, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (163, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (164, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (164, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (164, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (164, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (165, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (165, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (165, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (165, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (id, code) values (166, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (166, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (166, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (166, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (167, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (167, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (167, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (167, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (168, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (168, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (168, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (168, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (169, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (169, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (169, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (169, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (170, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (170, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (170, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (170, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (171, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (171, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (171, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (171, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (172, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (172, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (172, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (172, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (173, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (173, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (173, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (173, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (174, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (174, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (174, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (174, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (175, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (175, 'INVOICE_NUM', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (175, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (175, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (176, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (176, 'Acct_Desc', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (176, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (176, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (177, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (177, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (177, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (177, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (178, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (178, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (178, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (178, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (179, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (179, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (179, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (179, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (180, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (180, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (180, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (180, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (181, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (181, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (181, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (181, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (182, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (182, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (182, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (182, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (183, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (183, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (183, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (183, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (id, code) values (184, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (184, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (184, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (184, 'Acct_Desc', 'contains', 'tax');

  insert into paredown_rules (id, code) values (185, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (185, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (185, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (185, 'Item_Text', 'contains', 'tax');

  insert into paredown_rules (id, code) values (186, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (186, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (186, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (186, 'INVOICE_NUM', 'contains', 'MFT');

  insert into paredown_rules (id, code) values (187, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (187, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (187, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (187, 'Acct_Desc', 'contains', 'MFT');

  insert into paredown_rules (id, code) values (188, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (188, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (188, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (188, 'Item_Text', 'contains', 'MFT');

  insert into paredown_rules (id, code) values (189, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (189, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (189, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (189, 'INVOICE_NUM', 'contains', 'PST ');

  insert into paredown_rules (id, code) values (190, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (190, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (190, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (190, 'Acct_Desc', 'contains', 'PST ');

  insert into paredown_rules (id, code) values (191, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (191, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (191, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (191, 'Item_Text', 'contains', 'PST ');

  insert into paredown_rules (id, code) values (192, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (192, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (192, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (192, 'INVOICE_NUM', 'contains', 'CT');

  insert into paredown_rules (id, code) values (193, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (193, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (193, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (193, 'Acct_Desc', 'contains', 'CT');

  insert into paredown_rules (id, code) values (194, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (194, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (194, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (194, 'Item_Text', 'contains', 'CT');

  insert into paredown_rules (id, code) values (195, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (195, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (195, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (195, 'INVOICE_NUM', 'contains', 'GST');

  insert into paredown_rules (id, code) values (196, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (196, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (196, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (196, 'Acct_Desc', 'contains', 'GST');

  insert into paredown_rules (id, code) values (197, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (197, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (197, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (197, 'Item_Text', 'contains', 'GST');

  insert into paredown_rules (id, code) values (198, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (198, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (198, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (198, 'INVOICE_NUM', 'contains', 'QST');

  insert into paredown_rules (id, code) values (199, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (199, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (199, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (199, 'Acct_Desc', 'contains', 'QST');

  insert into paredown_rules (id, code) values (200, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (200, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (200, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (200, 'Item_Text', 'contains', 'QST');

  insert into paredown_rules (id, code) values (201, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (201, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (201, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (201, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (202, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (202, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (202, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (202, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (203, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (203, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (203, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (203, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (204, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (204, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (204, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (204, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (205, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (205, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (205, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (205, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (206, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (206, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (206, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (206, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (207, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (207, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (207, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (207, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (208, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (208, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (208, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (208, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (209, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (209, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (209, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (209, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (210, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (210, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (210, 'INVOICE_NUM', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (210, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (211, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (211, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (211, 'Acct_Desc', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (211, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (212, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (212, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (212, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (212, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (213, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (213, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (213, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (213, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (214, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (214, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (214, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (214, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (215, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (215, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (215, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (215, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (216, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (216, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (216, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (216, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (217, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (217, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (217, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (217, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (218, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (218, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (218, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (218, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (id, code) values (219, '208');
  insert into paredown_rules_conditions (rule_id, field, operator, value) values (219, 'Acct_Desc', 'contains', 'AP amount');
  "


##
