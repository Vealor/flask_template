sudo -i -u postgres psql <<EOF
drop database itra_db;
create database itra_db;
grant all privileges on database itra_db to itra;
EOF

source activate
rm ./migrations/versions/*.py
FLASK_ENV='development' flask db migrate
sleep 2
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
  insert into capsgen (user_id, project_id, is_completed) values (1, 1, False);
  insert into fx_rates (date, usdtocad) values ('2010-01-01', 1.56);
  insert into fx_rates (date, usdtocad) values ('2010-01-02', 1.57);
  insert into vendors (name) values ('miner buyer');
  insert into vendors (name) values ('banana buyer');
  insert into vendors (name) values ('potato buyer');
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 1, 1);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 2, 1);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 3, 1);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 1, 1);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 2, 1);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 3, 1);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 1, 2);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 2, 2);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 1, 3);
  insert into transactions (data, codes, vendor_id, project_id) values ('{}', '{}', 2, 3);
  insert into user_project (user_id, project_id) values (1, 1);
  insert into gst_registration(project_id, capsgen_id) values (1,1);

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



  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (1, 'Acct_Desc', 'contains', 'Donation');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (2, 'Item_Text', 'contains', 'Donation');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (3, 'INVOICE_NUM', 'contains', 'Donation');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (4, 'Acct_Desc', 'contains', 'Sponsorship');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (5, 'Item_Text', 'contains', 'Sponsorship');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (6, 'INVOICE_NUM', 'contains', 'Sponsorship');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (7, 'Acct_Desc', 'contains', 'Charity');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (8, 'Item_Text', 'contains', 'Charity');

  insert into paredown_rules (is_core, code) values ('t', '210');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (9, 'INVOICE_NUM', 'contains', 'Charity');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (10, 'Acct_Desc', 'contains', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (10, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (11, 'Item_Text', 'contains', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (11, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (12, 'INVOICE_NUM', 'contains', 'Insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (12, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (13, 'Acct_Desc', 'contains', 'Health');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (13, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (14, 'Item_Text', 'contains', 'Health');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (14, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (15, 'INVOICE_NUM', 'contains', 'Health');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (15, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (16, 'Acct_Desc', 'contains', 'Dental');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (16, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (17, 'Item_Text', 'contains', 'Dental');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (17, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (18, 'INVOICE_NUM', 'contains', 'Dental');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (18, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (19, 'Acct_Desc', 'contains', 'Disability');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (19, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (20, 'Item_Text', 'contains', 'Disability');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (20, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (21, 'INVOICE_NUM', 'contains', 'Disability');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (21, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (22, 'Acct_Desc', 'contains', 'LTD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (22, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (23, 'Item_Text', 'contains', 'LTD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (23, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (24, 'INVOICE_NUM', 'contains', 'LTD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (24, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (25, 'Acct_Desc', 'contains', 'STD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (25, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (26, 'Item_Text', 'contains', 'STD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (26, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (27, 'INVOICE_NUM', 'contains', 'STD');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (27, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (28, 'Acct_Desc', 'contains', 'Medical');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (28, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (29, 'Item_Text', 'contains', 'Medical');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (29, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (30, 'INVOICE_NUM', 'contains', 'Medical');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (30, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (31, 'Acct_Desc', 'contains', 'Medical Services Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (31, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (32, 'Item_Text', 'contains', 'Medical Services Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (32, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (33, 'Acct_Desc', 'contains', 'MSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (33, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (34, 'Item_Text', 'contains', 'MSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (34, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (35, 'INVOICE_NUM', 'contains', 'MSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (35, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (36, 'Acct_Desc', 'contains', 'Payroll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (36, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (37, 'Item_Text', 'contains', 'Payroll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (37, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (38, 'INVOICE_NUM', 'contains', 'Payroll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (38, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (39, 'Acct_Desc', 'contains', 'Salary');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (39, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (40, 'Item_Text', 'contains', 'Salary');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (40, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (41, 'INVOICE_NUM', 'contains', 'Salary');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (41, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (42, 'Acct_Desc', 'contains', 'Salaries');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (42, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (43, 'Item_Text', 'contains', 'Salaries');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (43, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (44, 'INVOICE_NUM', 'contains', 'Salaries');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (44, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (45, 'Acct_Desc', 'contains', 'Severance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (45, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (46, 'Item_Text', 'contains', 'Severance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (46, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (47, 'INVOICE_NUM', 'contains', 'Severance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (47, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (48, 'Acct_Desc', 'contains', 'Employment insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (48, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (49, 'Item_Text', 'contains', 'Employment insurance');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (49, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (50, 'Acct_Desc', 'contains', 'Employer Health Tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (50, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (51, 'Item_Text', 'contains', 'Employer Health Tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (51, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (52, 'Acct_Desc', 'contains', 'EHT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (52, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (53, 'Item_Text', 'contains', 'EHT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (53, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (54, 'INVOICE_NUM', 'contains', 'EHT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (54, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (55, 'Acct_Desc', 'contains', 'Garnish');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (55, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (56, 'Item_Text', 'contains', 'Garnish');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (56, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (57, 'INVOICE_NUM', 'contains', 'Garnish');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (57, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (58, 'Acct_Desc', 'contains', 'Share purchase');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (58, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (59, 'Item_Text', 'contains', 'Share purchase');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (59, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (60, 'Acct_Desc', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (60, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (61, 'Item_Text', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (61, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (62, 'INVOICE_NUM', 'contains', 'LTIP ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (62, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (63, 'Acct_Desc', 'contains', 'RRSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (63, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (64, 'Item_Text', 'contains', 'RRSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (64, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (65, 'INVOICE_NUM', 'contains', 'RRSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (65, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (66, 'Acct_Desc', 'contains', 'Work Safety');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (66, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (67, 'Item_Text', 'contains', 'Work Safety');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (67, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (68, 'Acct_Desc', 'contains', 'Workers Comp');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (68, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (69, 'Item_Text', 'contains', 'Workers Comp');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (69, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (70, 'Acct_Desc', 'contains', 'workers compensation board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (70, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (71, 'Item_Text', 'contains', 'workers compensation board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (71, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (72, 'Acct_Desc', 'contains', 'Worksafe BC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (72, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (73, 'Item_Text', 'contains', 'Worksafe BC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (73, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (74, 'Acct_Desc', 'contains', 'WorksafeBC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (74, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (75, 'Item_Text', 'contains', 'WorksafeBC');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (75, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (76, 'Acct_Desc', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (76, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (77, 'Item_Text', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (77, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (78, 'INVOICE_NUM', 'contains', 'BCMSP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (78, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (79, 'Acct_Desc', 'contains', 'WSIB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (79, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (80, 'Item_Text', 'contains', 'WSIB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (80, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (81, 'INVOICE_NUM', 'contains', 'WSIB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (81, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (82, 'Acct_Desc', 'contains', 'Workplace Safety & Insurance Board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (82, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (83, 'Item_Text', 'contains', 'Workplace Safety & Insurance Board');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (83, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (84, 'Acct_Desc', 'contains', 'Canada Pension Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (84, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (85, 'Item_Text', 'contains', 'Canada Pension Plan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (85, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (86, 'Acct_Desc', 'contains', 'WCB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (86, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (87, 'Item_Text', 'contains', 'WCB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (87, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (88, 'INVOICE_NUM', 'contains', 'WCB');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (88, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (89, 'Acct_Desc', 'contains', 'Union due');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (89, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (90, 'Item_Text', 'contains', 'Union due');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (90, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (91, 'Acct_Desc', 'contains', 'Pension');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (91, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (92, 'Item_Text', 'contains', 'Pension');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (92, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (93, 'INVOICE_NUM', 'contains', 'Pension');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (93, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (94, 'Acct_Desc', 'contains', 'Dividends');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (94, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (95, 'Item_Text', 'contains', 'Dividends');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (95, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (96, 'INVOICE_NUM', 'contains', 'Dividends');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (96, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (97, 'Acct_Desc', 'contains', 'EI ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (97, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (98, 'Item_Text', 'contains', 'EI ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (98, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (99, 'Acct_Desc', 'contains', 'CPP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (99, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (100, 'Item_Text', 'contains', 'CPP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (100, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Payroll / Benefits');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (101, 'INVOICE_NUM', 'contains', 'CPP');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (101, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (102, 'Acct_Desc', 'contains', 'Loan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (102, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (103, 'Item_Text', 'contains', 'Loan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (103, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (104, 'INVOICE_NUM', 'contains', 'Loan');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (104, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (105, 'Acct_Desc', 'contains', 'Debt');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (105, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (106, 'Item_Text', 'contains', 'Debt');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (106, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (107, 'INVOICE_NUM', 'contains', 'Debt');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (107, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (108, 'Acct_Desc', 'contains', 'Interest');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (108, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (109, 'Item_Text', 'contains', 'Interest');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (109, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '209');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (110, 'INVOICE_NUM', 'contains', 'Interest');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (110, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Tolls');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (111, 'Acct_Desc', 'contains', 'Toll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (111, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code, comment) values ('t', '221', 'Tolls');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (112, 'Item_Text', 'contains', 'Toll');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (112, 'VEND_EFF_RATE_N', '<', '1');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (113, 'INVOICE_NUM', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (113, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (113, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (114, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (114, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (114, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (115, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (115, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (115, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (116, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (116, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (116, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (117, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (117, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (117, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (118, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (118, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (118, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (119, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (119, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (119, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (120, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (120, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (120, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (121, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (121, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (121, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (122, 'INVOICE_NUM', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (122, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (122, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (123, 'Acct_Desc', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (123, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (123, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (124, 'Item_Text', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (124, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (124, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (125, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (125, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (125, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (126, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (126, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (126, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (127, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (127, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (127, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (128, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (128, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (128, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (129, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (129, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (129, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (130, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (130, 'SUPPLIER_NAME', 'contains', 'Receiver General ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (130, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (131, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (131, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (131, 'Acct_Desc', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (132, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (132, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (132, 'Item_Text', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (133, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (133, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (133, 'INVOICE_NUM', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (134, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (134, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (134, 'Acct_Desc', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (135, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (135, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (135, 'Item_Text', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (136, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (136, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (136, 'INVOICE_NUM', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (137, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (137, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (137, 'Acct_Desc', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (138, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (138, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (138, 'Item_Text', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (139, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (139, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (139, 'INVOICE_NUM', 'contains', 'CT ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (140, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (140, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (140, 'Acct_Desc', 'contains', 'CT ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (141, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (141, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (141, 'Item_Text', 'contains', 'CT ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (142, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (142, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (142, 'INVOICE_NUM', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (143, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (143, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (143, 'Acct_Desc', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (144, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (144, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (144, 'Item_Text', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (145, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (145, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (145, 'INVOICE_NUM', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (146, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (146, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (146, 'Acct_Desc', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (147, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (147, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (147, 'Item_Text', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (148, 'SUPPLIER_NAME', 'contains', 'Ministry');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (148, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (148, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (149, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (149, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (149, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (150, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (150, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (150, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (151, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (151, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (151, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (152, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (152, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (152, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (153, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (153, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (153, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (154, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (154, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (154, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (155, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (155, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (155, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (156, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (156, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (156, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (157, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (157, 'INVOICE_NUM', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (157, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (158, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (158, 'Acct_Desc', 'contains', 'CT ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (158, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (159, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (159, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (159, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (160, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (160, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (160, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (161, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (161, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (161, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (162, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (162, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (162, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (163, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (163, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (163, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (164, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (164, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (164, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (165, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (165, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (165, 'SUPPLIER_NAME', 'contains', 'CRA');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (166, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (166, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (166, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (167, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (167, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (167, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (168, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (168, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (168, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (169, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (169, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (169, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (170, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (170, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (170, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (171, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (171, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (171, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (172, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (172, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (172, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (173, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (173, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (173, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (174, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (174, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (174, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (175, 'INVOICE_NUM', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (175, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (175, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (176, 'Acct_Desc', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (176, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (176, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (177, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (177, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (177, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (178, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (178, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (178, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (179, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (179, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (179, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (180, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (180, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (180, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (181, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (181, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (181, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (182, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (182, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (182, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (183, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (183, 'SUPPLIER_NAME', 'contains', 'Canada Revenue');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (183, 'Acct_Desc', 'contains', 'AP amount');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (184, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (184, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (184, 'Acct_Desc', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (185, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (185, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (185, 'Item_Text', 'contains', 'tax');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (186, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (186, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (186, 'INVOICE_NUM', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (187, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (187, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (187, 'Acct_Desc', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (188, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (188, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (188, 'Item_Text', 'contains', 'MFT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (189, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (189, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (189, 'INVOICE_NUM', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (190, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (190, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (190, 'Acct_Desc', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (191, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (191, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (191, 'Item_Text', 'contains', 'PST ');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (192, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (192, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (192, 'INVOICE_NUM', 'contains', 'CT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (193, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (193, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (193, 'Acct_Desc', 'contains', 'CT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (194, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (194, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (194, 'Item_Text', 'contains', 'CT');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (195, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (195, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (195, 'INVOICE_NUM', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (196, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (196, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (196, 'Acct_Desc', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (197, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (197, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (197, 'Item_Text', 'contains', 'GST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (198, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (198, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (198, 'INVOICE_NUM', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (199, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (199, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (199, 'Acct_Desc', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (200, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (200, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (200, 'Item_Text', 'contains', 'QST');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (201, 'SUPPLIER_NAME', 'contains', 'Canada Customs');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (201, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (201, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (202, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (202, 'Acct_Desc', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (202, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (203, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (203, 'Item_Text', 'contains', 'tax');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (203, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (204, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (204, 'INVOICE_NUM', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (204, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (205, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (205, 'Acct_Desc', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (205, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (206, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (206, 'Item_Text', 'contains', 'MFT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (206, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (207, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (207, 'INVOICE_NUM', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (207, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (208, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (208, 'Acct_Desc', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (208, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (209, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (209, 'Item_Text', 'contains', 'PST ');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (209, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (210, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (210, 'INVOICE_NUM', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (210, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (211, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (211, 'Acct_Desc', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (211, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (212, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (212, 'Item_Text', 'contains', 'CT');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (212, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (213, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (213, 'INVOICE_NUM', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (213, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (214, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (214, 'Acct_Desc', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (214, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (215, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (215, 'Item_Text', 'contains', 'GST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (215, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (216, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (216, 'INVOICE_NUM', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (216, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (217, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (217, 'Acct_Desc', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (217, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (218, 'Acct_Desc', 'contains', 'AP amount');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (218, 'Item_Text', 'contains', 'QST');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (218, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec');

  insert into paredown_rules (is_core, code) values ('t', '208');
  insert into paredown_rules_conditions (paredown_rule_id, field, operator, value) values (219, 'Acct_Desc', 'contains', 'AP amount');

"
sleep 2
psql -h localhost -U itra itra_db -c "
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bkpf_belnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('doc_type_gl','Doc Type (GL)','FALSE','FALSE','dt_varchar','2','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('inv_date','Inv Date','FALSE','FALSE','dt_varchar','8','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('post_date_gl','Post Date (GL)','FALSE','FALSE','dt_varchar','8','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bkpf_bukrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bkpf_gjahr_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('fx_rate','FX Rate','FALSE','FALSE','dt_varchar','9(5)','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bkpf_kzwrs_key',NULL,'FALSE','FALSE','dt_varchar','5',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('fiscal_period_gl','Fiscal Period (GL)','FALSE','FALSE','dt_varchar','2','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('trnx_code_gl','Trnx Code (GL)','FALSE','FALSE','dt_varchar','20','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ccy','CCY','FALSE','FALSE','dt_varchar','5','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('inv_num','Inv #','FALSE','FALSE','dt_varchar','16','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_augbl_key',NULL,'FALSE','TRUE','dt_varchar','10',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_augdt_key',NULL,'FALSE','TRUE','dt_varchar','8',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_belnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_bukrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_buzei_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_gjahr_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bsak_lifnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('spec_trnx_type_gl','Spec Trnx Type (GL)','FALSE','TRUE','dt_varchar','1','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('spec_indicator_gl','Spec Indicator (GL)','FALSE','TRUE','dt_varchar','1','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cash_disc_percent_1_gl','Cash Disc % 1 (GL)','FALSE','FALSE','dt_varchar','5(3)','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cash_disc_days_1_gl','Cash Disc Days 1 (GL)','FALSE','FALSE','dt_varchar','3','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cash_disc_percent_2_gl','Cash Disc % 2 (GL)','FALSE','FALSE','dt_varchar','5(3)','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cash_disc_days_2_gl','Cash Disc Days 2 (GL)','FALSE','FALSE','dt_varchar','3','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('pymt_period_gl','Pymt Period (GL)','FALSE','FALSE','dt_varchar','3','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('pymt_terms_gl','Pymt Terms (GL)','FALSE','FALSE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('assign_num_gl','Assign # (GL)','FALSE','TRUE','dt_varchar','18','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('main_asset_num','Main Asset #','FALSE','FALSE','dt_varchar','12','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('asset_sub_num','Asset Sub #','FALSE','FALSE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('gl_doc_num','GL Doc #','FALSE','TRUE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('post_key_gl','Post Key (GL)','FALSE','FALSE','dt_varchar','2','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('gl_doc_status','GL Doc Status','FALSE','FALSE','dt_varchar','1','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bseg_budat_key',NULL,'FALSE','FALSE','dt_varchar','8',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('co_code_gl','Co Code (GL)','FALSE','TRUE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bseg_buzei_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('amount_local_ccy','Amount, Local CCY','FALSE','FALSE','dt_varchar','13(2)','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('po_doc_num','PO Doc #','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bseg_ebelp_key',NULL,'FALSE','FALSE','dt_varchar','5',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('func_area_gl','Func Area (GL)','FALSE','FALSE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('fiscal_year_gl','Fiscal Yr (GL)','FALSE','TRUE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bus_area_dept_num_gl','Bus Area / Dept # (GL)','FALSE','FALSE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('largest_debit_half_acct_num_gl','Largest Debit 1/2 Acct # (GL)','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('control_area_gl','Control Area (GL)','FALSE','FALSE','dt_varchar','4','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cost_ctr_num_gl','Cost Ctr # (GL)','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cx_num','Customer #','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_num','Vendor #','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('material_num_gl','Material # (GL)','FALSE','FALSE','dt_varchar','18','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tax_type_gl','Tx Type (GL)','FALSE','FALSE','dt_varchar','1','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bseg_mwsk3_key',NULL,'FALSE','FALSE','dt_varchar','2',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('po_tax_code_gl','PO Tx Code (GL)','FALSE','FALSE','dt_varchar','2','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('gst_hst_qst_pst_local_ccy','GST/HST-QST-PST, Local CCY','FALSE','FALSE','dt_varchar','13(2)','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bseg_pargb_key',NULL,'FALSE','FALSE','dt_varchar','4',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('profit_ctr_num','Profit Ctr #','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('wbs_gl','WBS (GL)','FALSE','FALSE','dt_varchar','8','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('item_descr_gl','Item Descr (GL)','FALSE','FALSE','dt_varchar','50','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('reverse_doc_num','Reverse Doc # (GL)','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('reverse_reason_gl','Reverse Reason (GL)','FALSE','FALSE','dt_varchar','2','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tax_jur_gl','Tx Jur (GL)','FALSE','FALSE','dt_varchar','15','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('sales_doc_num_gl','Sales Doc # (GL)','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('billing_doc_num','Billing Doc #','FALSE','FALSE','dt_varchar','10','sales','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('gst_hst_pst_qst_doc_ccy','GST/HST-QST-PST, Doc CCY','FALSE','FALSE','dt_varchar','13(2)','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ap_ar_amt_doc_ccy','AP/AR Amount, Doc CCY','FALSE','FALSE','dt_varchar','13(2)','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cepc_datbi_key',NULL,'FALSE','TRUE','dt_varchar','8',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cepc_kokrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cepc_prctr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('profit_ctr_tx_jur','Profit Ctr Tx Jur','FALSE','FALSE','dt_varchar','15','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('profit_ctr_name','Profit Ctr Name','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('profit_ctr_descr','Profit Ctr Descr','FALSE','FALSE','dt_varchar','10','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cepct_prctr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cepct_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('csks_datbi_key',NULL,'FALSE','TRUE','dt_varchar','8',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('csks_kokrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('csks_kostl_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cost_ctr_tx_jur','Cost Ctr Tx Jur','FALSE','FALSE','dt_varchar','15','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cskt_datbi_key',NULL,'FALSE','TRUE','dt_varchar','8',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cskt_kokrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cskt_kostl_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cost_ctr_name','Cost Ctr Name','FALSE','FALSE','dt_varchar','20','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cost_ctr_descr','Cost Ctr Descr','FALSE','FALSE','dt_varchar','40','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cskt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ska1_bukrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ska1_ktopl_key',NULL,'FALSE','TRUE','dt_varchar','4',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ska1_saknr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('skat_ktopl_key',NULL,'FALSE','TRUE','dt_varchar','4',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('skat_saknr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('skat_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl','Largest Debit 1 Acct # (GL)/ Largest Debit 2 Acct # (GL)','FALSE','FALSE','dt_varchar','50','caps_basic','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('skb1_bukrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('skb1_saknr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t003t_blart_key',NULL,'FALSE','TRUE','dt_varchar','2','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('doc_type_descr','Doc Type Descr','FALSE','FALSE','dt_varchar','20','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t003t_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tbslt_bschl_key',NULL,'FALSE','TRUE','dt_varchar','2',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('post_key_descr','Post Key Descr','FALSE','FALSE','dt_varchar','20','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tbslt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tbslt_umskz_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ccy_descr','CCY Descr','FALSE','FALSE','dt_varchar','15','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tcurt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tcurt_waers_key',NULL,'FALSE','TRUE','dt_varchar','5','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tgsbt_gsber_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bus_area_dept_name_gl','Bus Area / Dept Name (GL)','FALSE','FALSE','dt_varchar','30','caps_advanced','accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tgsbt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'accounting');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ekko_ebeln_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('punch_grp_po','Purch Group (PO)','FALSE','FALSE','dt_varchar','3','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('punch_org_po','Purch Org (PO)','FALSE','FALSE','dt_varchar','4','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('handover_loc_po','Handover Loc (PO)','FALSE','FALSE','dt_varchar','10','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_phone','Vend Phone','FALSE','FALSE','dt_varchar','16','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_person','Vend Person','FALSE','FALSE','dt_varchar','30','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('wbs_po','WBS (PO)','FALSE','FALSE','dt_varchar','8','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ekpo_ebeln_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ekpo_ebelp_key',NULL,'FALSE','TRUE','dt_varchar','5',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ekpo_ematn_key',NULL,'FALSE','FALSE','dt_varchar','18','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ekpo_lgort_key',NULL,'FALSE','FALSE','dt_varchar','4',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('po_tx_code_po','PO Tx Code (PO)','FALSE','FALSE','dt_varchar','2','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('plant_num','Plant #','FALSE','FALSE','dt_varchar','4','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('po_tx_jur','PO Tx Jur','FALSE','FALSE','dt_varchar','15','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('po_item_descr','PO Item Descr','FALSE','FALSE','dt_varchar','40','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lfa1_land1_key',NULL,'FALSE','FALSE','dt_varchar','3',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lfa1_lifnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_name','Vend Name','FALSE','FALSE','dt_varchar','35','caps_basic','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_city','Vend City','FALSE','FALSE','dt_varchar','35','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_region','Vend Region','FALSE','FALSE','dt_varchar','3','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_tax_num_1','Vend Tax #1','FALSE','FALSE','dt_varchar','16','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_tax_num_2','Vend Tax #2','FALSE','FALSE','dt_varchar','11','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_tax_num_3','Vend Tax #3','FALSE','FALSE','dt_varchar','18','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_tax_num_4','Vend Tax #4','FALSE','FALSE','dt_varchar','18','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_tax_num_5','Vend Tax #5','FALSE','FALSE','dt_varchar','60','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_tax_num_type','Vend Tax # Type','FALSE','FALSE','dt_varchar','2','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('vend_reg_num','Vend Reg #','FALSE','FALSE','dt_varchar','20','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lfas_land1_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lfas_lifnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lfm1_ekorg_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('incoterms1','Incoterms1','FALSE','FALSE','dt_varchar','3','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('incoterms2','Incoterms2','FALSE','FALSE','dt_varchar','28','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('lfm1_lifnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t024_ekgrp_key',NULL,'FALSE','TRUE','dt_varchar','3','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('purch_group_descr_po','Purch Group Descr (PO)','FALSE','FALSE','dt_varchar','18','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t024e_ekorg_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('purch_org_descr_po','Purch Org Descr (PO)','FALSE','FALSE','dt_varchar','18','caps_advanced','purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('toa01_arc_doc_id_key',NULL,'FALSE','TRUE','dt_varchar','40',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('toa01_archiv_id_key',NULL,'FALSE','TRUE','dt_varchar','2',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('toa01_object_id_key',NULL,'FALSE','TRUE','dt_varchar','50',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('toa01_sap_object_key',NULL,'FALSE','TRUE','dt_varchar','10',NULL,'purchases');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_descr_mat','Mat Descr (MAT)','FALSE','FALSE','dt_varchar','40','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('makt_matnr_key',NULL,'FALSE','TRUE','dt_varchar','18','repetition','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ean_upc_num_mat','EAN/UPC # (MAT)','FALSE','FALSE','dt_varchar','18','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mara_gewei_key',NULL,'FALSE','FALSE','dt_varchar','3',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_orig_ctry_mat','Mat Orig Country (MAT)','FALSE','FALSE','dt_varchar','3','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mara_magrv_key',NULL,'FALSE','FALSE','dt_varchar','4',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mara_matkl_key',NULL,'FALSE','FALSE','dt_varchar','9',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mara_matnr_key',NULL,'FALSE','TRUE','dt_varchar','18','repetition','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mara_mfrnr_key',NULL,'FALSE','FALSE','dt_varchar','10',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ean_categ_mat','EAN Categ (MAT)','FALSE','FALSE','dt_varchar','2','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_tx_class_mat','Mat Tx Class (MAT)','FALSE','FALSE','dt_varchar','1','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mara_voleh_key',NULL,'FALSE','FALSE','dt_varchar','3',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_dept_ctry_mat','Mat Dept Country (MAT)','FALSE','TRUE','dt_varchar','3','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mlan_matnr_key',NULL,'FALSE','TRUE','dt_varchar','18','repetition','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_tx_ind_mat','Mat Tx Ind (MAT)','FALSE','FALSE','dt_varchar','1','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mseg_ebeln_key',NULL,'FALSE','FALSE','dt_varchar','10','repetition','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mseg_ebelp_key',NULL,'FALSE','FALSE','dt_varchar','5',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_doc_num_mat','Mat Doc # (MAT)','FALSE','TRUE','dt_varchar','10','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mseg_mjahr_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_plnt_mat','Mat Plant (MAT)','FALSE','FALSE','dt_varchar','4','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mseg_zeile_key',NULL,'FALSE','TRUE','dt_varchar','4',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('stor_loc_desc_mat','Stor Loc Desc (MAT)','FALSE','FALSE','dt_varchar','16','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('stor_loc_mat','Stor Loc (MAT)','FALSE','TRUE','dt_varchar','4','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('stor_plant_mat','Stor Plant (MAT)','FALSE','TRUE','dt_varchar','4','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t006a_msehi_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t006a_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t023t_matkl_key',NULL,'FALSE','TRUE','dt_varchar','9',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t023t_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_group_descr_mat','Mat Group Descr (MAT)','FALSE','FALSE','dt_varchar','20','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tmkm1t_land1_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tmkm1t_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_tx_ind_descr_mat','Mat Tx Ind Descr (MAT)','FALSE','FALSE','dt_varchar','20','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ean_categ_descr_mat','EAN Categ Descr (MAT)','FALSE','FALSE','dt_varchar','40','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tntpb_numtp_key',NULL,'FALSE','TRUE','dt_varchar','2','repetition','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tntpb_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tskmt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tskmt_tatyp_key',NULL,'FALSE','TRUE','dt_varchar','4',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tskmt_taxkm_key',NULL,'FALSE','FALSE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('mat_tx_class_descr_mat','Mat Tx Class Descr (MAT)','FALSE','FALSE','dt_varchar','20','caps_advanced','materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tvegrt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tvtyt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tvtyt_traty_key',NULL,'FALSE','TRUE','dt_varchar','4',NULL,'materials');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_descr_proj','Proj Descr (PROJ)','FALSE','FALSE','dt_varchar','40','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_defin_proj','Proj Defin (PROJ)','FALSE','FALSE','dt_varchar','24','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_internal_proj','Proj Internal # (PROJ)','FALSE','TRUE','dt_varchar','8','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_tx_jur_proj','Proj Tx Jur (PROJ)','FALSE','FALSE','dt_varchar','15','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_mngr_name_proj','Proj Mngr Name (PROJ)','FALSE','FALSE','dt_varchar','25','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_mngr_num_proj','Proj Mngr # (PROJ)','FALSE','FALSE','dt_varchar','8','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('bus_area_proj','Bus Area (PROJ)','FALSE','FALSE','dt_varchar','4','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('plant_proj','Plant (PROJ)','FALSE','FALSE','dt_varchar','4','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('object_num_proj','Object # (PROJ)','FALSE','FALSE','dt_varchar','22','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('jv_obj_type_proj','JV Obj Type (PROJ)','FALSE','FALSE','dt_varchar','4','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('wbs_bus_area_proj','WBS Bus Area (PROJ)','FALSE','FALSE','dt_varchar','4','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('wbs_cntrl_area_proj','WBS Control Area (PROJ)','FALSE','FALSE','dt_varchar','4','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('wbs_elem_id_proj','WBS Element ID (PROJ)','FALSE','FALSE','dt_varchar','24','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('wbs_elem_descr_proj','WBS Element Descr (PROJ)','FALSE','FALSE','dt_varchar','40','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_type_proj','Proj Type (PROJ)','FALSE','FALSE','dt_varchar','2','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('prps_psphi_key',NULL,'FALSE','FALSE','dt_varchar','8',NULL,'project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('prps_pspnr_key',NULL,'FALSE','TRUE','dt_varchar','8','repetition','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('proj_loc_proj','Proj Loc (PROJ)','FALSE','FALSE','dt_varchar','10','caps_advanced','project_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('check_num_pmt','Check # (PMT)','FALSE','TRUE','dt_varchar','13','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('payr_hbkid_key',NULL,'FALSE','TRUE','dt_varchar','5',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('payr_rzawe_key',NULL,'FALSE','TRUE','dt_varchar','13',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('pymt_dt_pmt','Pymt Date (PMT)','FALSE','FALSE','dt_varchar','8','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('payr_zbukr_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('pymt_doc_num_pmt','Pymt Doc # (PMT)','FALSE','TRUE','dt_varchar','10','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_bukrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_buzei_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_ebeln_key',NULL,'FALSE','FALSE','dt_varchar','10','repetition','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_ebelp_key',NULL,'FALSE','FALSE','dt_varchar','5',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('payee_code_pmt','Payee Code (PMT)','FALSE','TRUE','dt_varchar','16','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_gjahr_key',NULL,'FALSE','TRUE','dt_varchar','4',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_hkont_key',NULL,'FALSE','FALSE','dt_varchar','10',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cx_num_pmt','Customer # (PMT)','FALSE','TRUE','dt_varchar','10','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_laufd_key',NULL,'FALSE','TRUE','dt_varchar','8',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_laufi_key',NULL,'FALSE','TRUE','dt_varchar','6',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_lifnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_saknr_key',NULL,'FALSE','FALSE','dt_varchar','10',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_vblnr_key',NULL,'FALSE','TRUE','dt_varchar','10','repetition','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_xvorl_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('co_code_pmt','Co Code (PMT)','FALSE','TRUE','dt_varchar','4','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('regup_zlsch_key',NULL,'FALSE','FALSE','dt_varchar','1','repetition','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t042zt_land1_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t042zt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('pymt_method_pmt','Pymt Method (PMT)','FALSE','FALSE','dt_varchar','30','caps_advanced','payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t042zt_zlsch_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'payment_details');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('j_1atodct_j_1atodct_key',NULL,'FALSE','TRUE','dt_varchar','2',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('j_1atodct_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tx_type_descr_tx','Tx Type Descr (TX)','FALSE','FALSE','dt_varchar','30','caps_advanced','tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t005s_bland_key',NULL,'FALSE','FALSE','dt_varchar','3',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('prov_tx_code_tx','Prov Tx Code (TX)','FALSE','FALSE','dt_varchar','3','caps_advanced','tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t005s_land1_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t007a_kalsm_key',NULL,'FALSE','TRUE','dt_varchar','6',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t007a_mwskz_key',NULL,'FALSE','TRUE','dt_varchar','2',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t007s_kalsm_key',NULL,'FALSE','TRUE','dt_varchar','6',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t007s_mwskz_key',NULL,'FALSE','TRUE','dt_varchar','2',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t007s_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tx_name_tx','Tax Name (TX)','FALSE','FALSE','dt_varchar','50','caps_advanced','tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ttxjt_kalsm_key',NULL,'FALSE','TRUE','dt_varchar','6',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ttxjt_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tx_jur_descr_tx','Tax Jur Descr (TX)','FALSE','FALSE','dt_varchar','50','caps_advanced','tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('ttxjt_txjcd_key',NULL,'FALSE','TRUE','dt_varchar','15',NULL,'tax');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t001_bukrs_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('co_name','Co Name','FALSE','FALSE','dt_varchar','25','caps_basic','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t001_land1_key',NULL,'FALSE','FALSE','dt_varchar','3',NULL,'other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('plant_name_plant','Plant Name (PLANT)','FALSE','FALSE','dt_varchar','30','caps_advanced','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('plant_tx_jur_plant','Plant Tx Jur (PLANT)','FALSE','FALSE','dt_varchar','15','caps_advanced','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t001w_werks_key',NULL,'FALSE','TRUE','dt_varchar','4','repetition','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t005t_land1_key',NULL,'FALSE','TRUE','dt_varchar','3',NULL,'other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('cntry_name','Country Name','FALSE','FALSE','dt_varchar','15','caps_advanced','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('t005t_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('incoterms1_descr','Incoterms1 Descr','FALSE','FALSE','dt_varchar','3','caps_advanced','other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tinct_inco1_key',NULL,'FALSE','FALSE','dt_varchar','3',NULL,'other');
INSERT INTO cdm_labels(script_label,display_name,is_calculated,is_unique,datatype,length,caps_interface,category) VALUES ('tinct_spras_key',NULL,'FALSE','TRUE','dt_varchar','1',NULL,'other');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BELNR',1,'bkpf_belnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BLART',1,'doc_type_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BLDAT',1,'inv_date');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BUDAT',1,'post_date_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BUKRS',1,'bkpf_bukrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','GJAHR',1,'bkpf_gjahr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','KURSF',1,'fx_rate');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','KZWRS',1,'bkpf_kzwrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','MONAT',1,'fiscal_period_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','TCODE',1,'trnx_code_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','WAERS',1,'ccy');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','XBLNR',1,'inv_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','AUGBL',1,'bsak_augbl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','AUGDT',1,'bsak_augdt_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','BELNR',1,'bsak_belnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','BUKRS',1,'bsak_bukrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','BUZEI',1,'bsak_buzei_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','GJAHR',1,'bsak_gjahr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','LIFNR',1,'bsak_lifnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','UMSKS',1,'spec_trnx_type_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','UMSKZ',1,'spec_indicator_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZBD1P',1,'cash_disc_percent_1_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZBD1T',1,'cash_disc_days_1_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZBD2P',1,'cash_disc_percent_2_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZBD2T',1,'cash_disc_days_2_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZBD3T',1,'pymt_period_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZTERM',1,'pymt_terms_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSAK','ZUONR',1,'assign_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','ANLN1',1,'main_asset_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','ANLN2',1,'asset_sub_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BELNR',1,'gl_doc_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BSCHL',1,'post_key_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BSTAT',1,'gl_doc_status');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BUDAT',1,'bseg_budat_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BUKRS',1,'co_code_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BUZEI',1,'bseg_buzei_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','DMBTR',1,'amount_local_ccy');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','EBELN',1,'po_doc_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','EBELP',1,'bseg_ebelp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','FKBER',1,'func_area_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','GJAHR',1,'fiscal_year_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','GSBER',1,'bus_area_dept_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','HKONT',1,'largest_debit_half_acct_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','KOKRS',1,'control_area_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','KOSTL',1,'cost_ctr_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','KUNNR',1,'cx_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','LIFNR',1,'vend_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MATNR',1,'material_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MWART',1,'tax_type_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MWSK3',1,'bseg_mwsk3_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MWSKZ',1,'po_tax_code_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MWSTS',1,'gst_hst_qst_pst_local_ccy');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','PARGB',1,'bseg_pargb_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','PRCTR',1,'profit_ctr_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','PROJK',1,'wbs_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','SGTXT',1,'item_descr_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','STBLG',1,'reverse_doc_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','STGRD',1,'reverse_reason_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','TXJCD',1,'tax_jur_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','VBEL2',1,'sales_doc_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','VBELN',1,'billing_doc_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','WMWST',1,'gst_hst_pst_qst_doc_ccy');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','WRBTR',1,'ap_ar_amt_doc_ccy');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPC','DATBI',1,'cepc_datbi_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPC','KOKRS',1,'cepc_kokrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPC','PRCTR',1,'cepc_prctr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPC','TXJCD',1,'profit_ctr_tx_jur');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPCT','KTEXT',1,'profit_ctr_name');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPCT','LTEXT',1,'profit_ctr_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPCT','PRCTR',1,'cepct_prctr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPCT','SPRAS',1,'cepct_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','DATBI',1,'csks_datbi_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','KOKRS',1,'csks_kokrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','KOSTL',1,'csks_kostl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','TXJCD',1,'cost_ctr_tx_jur');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','DATBI',1,'cskt_datbi_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KOKRS',1,'cskt_kokrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KOSTL',1,'cskt_kostl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KTEXT',1,'cost_ctr_name');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','LTEXT',1,'cost_ctr_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','SPRAS',1,'cskt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKA1','BUKRS',1,'ska1_bukrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKA1','KTOPL',1,'ska1_ktopl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKA1','SAKNR',1,'ska1_saknr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','KTOPL',1,'skat_ktopl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','SAKNR',1,'skat_saknr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','SPRAS',1,'skat_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','TXT50',1,'lrg_deb_1_acct_num_gl_lrg_deb_2_acct_num_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKB1','BUKRS',1,'skb1_bukrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKB1','SAKNR',1,'skb1_saknr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T003T','BLART',1,'t003t_blart_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T003T','LTEXT',1,'doc_type_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T003T','SPRAS',1,'t003t_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TBSLT','BSCHL',1,'tbslt_bschl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TBSLT','LTEXT',1,'post_key_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TBSLT','SPRAS',1,'tbslt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TBSLT','UMSKZ',1,'tbslt_umskz_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TCURT','KTEXT',1,'ccy_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TCURT','SPRAS',1,'tcurt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TCURT','WAERS',1,'tcurt_waers_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TGSBT','GSBER',1,'tgsbt_gsber_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TGSBT','GTEXT',1,'bus_area_dept_name_gl');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TGSBT','SPRAS',1,'tgsbt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKKO','EBELN',1,'ekko_ebeln_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKKO','EKGRP',1,'punch_grp_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKKO','EKORG',1,'punch_org_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKKO','HANDOVERLOC',1,'handover_loc_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKKO','TELF1',1,'vend_phone');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKKO','VERKF',1,'vend_person');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','DISUB_PSPNR',1,'wbs_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EBELN',1,'ekpo_ebeln_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EBELP',1,'ekpo_ebelp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EMATN',1,'ekpo_ematn_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','LGORT',1,'ekpo_lgort_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','MWSKZ',1,'po_tx_code_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','WERKS',1,'plant_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','TXJCD',1,'po_tx_jur');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','TXZ01',1,'po_item_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','LAND1',1,'lfa1_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','LIFNR',1,'lfa1_lifnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','NAME1',1,'vend_name');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','ORT01',1,'vend_city');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','REGIO',1,'vend_region');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCD1',1,'vend_tax_num_1');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCD2',1,'vend_tax_num_2');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCD3',1,'vend_tax_num_3');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCD4',1,'vend_tax_num_4');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCD5',1,'vend_tax_num_5');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCDT',1,'vend_tax_num_type');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCEG',1,'vend_reg_num');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFAS','LAND1',1,'lfas_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFAS','LIFNR',1,'lfas_lifnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFM1','EKORG',1,'lfm1_ekorg_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFM1','INCO1',1,'incoterms1');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFM1','INCO2',1,'incoterms2');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFM1','LIFNR',1,'lfm1_lifnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T024','EKGRP',1,'t024_ekgrp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T024','EKNAM',1,'purch_group_descr_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T024E','EKORG',1,'t024e_ekorg_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T024E','EKOTX',1,'purch_org_descr_po');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TOA01','ARC_DOC_ID',1,'toa01_arc_doc_id_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TOA01','ARCHIV_ID',1,'toa01_archiv_id_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TOA01','OBJECT_ID',1,'toa01_object_id_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TOA01','SAP_OBJECT',1,'toa01_sap_object_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','MAKTX',1,'mat_descr_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','MATNR',1,'makt_matnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','EAN11',1,'ean_upc_num_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','GEWEI',1,'mara_gewei_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','HERKL',1,'mat_orig_ctry_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','MAGRV',1,'mara_magrv_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','MATKL',1,'mara_matkl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','MATNR',1,'mara_matnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','MFRNR',1,'mara_mfrnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','NUMTP',1,'ean_categ_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','TAKLV',1,'mat_tx_class_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','VOLEH',1,'mara_voleh_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MLAN','ALAND',1,'mat_dept_ctry_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MLAN','MATNR',1,'mlan_matnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MLAN','TAXIM',1,'mat_tx_ind_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MSEG','EBELN',1,'mseg_ebeln_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MSEG','EBELP',1,'mseg_ebelp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MSEG','MBLNR',1,'mat_doc_num_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MSEG','MJAHR',1,'mseg_mjahr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MSEG','WERKS',1,'mat_plnt_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MSEG','ZEILE',1,'mseg_zeile_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001L','LGOBE',1,'stor_loc_desc_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001L','LGORT',1,'stor_loc_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001L','WERKS',1,'stor_plant_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T006A','MSEHI',1,'t006a_msehi_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T006A','SPRAS',1,'t006a_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T023T','MATKL',1,'t023t_matkl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T023T','SPRAS',1,'t023t_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T023T','WGBEZ',1,'mat_group_descr_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TMKM1T','LAND1',1,'tmkm1t_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TMKM1T','SPRAS',1,'tmkm1t_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TMKM1T','TAXIB',1,'mat_tx_ind_descr_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TNTPB','NTBEZ',1,'ean_categ_descr_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TNTPB','NUMTP',1,'tntpb_numtp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TNTPB','SPRAS',1,'tntpb_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TSKMT','SPRAS',1,'tskmt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TSKMT','TATYP',1,'tskmt_tatyp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TSKMT','TAXKM',1,'tskmt_taxkm_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TSKMT','VTEXT',1,'mat_tx_class_descr_mat');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TVEGRT','SPRAS',1,'tvegrt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TVTYT','SPRAS',1,'tvtyt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TVTYT','TRATY',1,'tvtyt_traty_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','POST1',1,'proj_descr_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','PSPID',1,'proj_defin_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','PSPNR',1,'proj_internal_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','TXJCD',1,'proj_tx_jur_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','VERNA',1,'proj_mngr_name_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','VERNR',1,'proj_mngr_num_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','VGSBR',1,'bus_area_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PROJ','WERKS',1,'plant_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','OBJNR',1,'object_num_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','OTYPE',1,'jv_obj_type_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','PGSBR',1,'wbs_bus_area_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','PKOKR',1,'wbs_cntrl_area_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','POSID',1,'wbs_elem_id_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','POST1',1,'wbs_elem_descr_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','PRART',1,'proj_type_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','PSPHI',1,'prps_psphi_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','PSPNR',1,'prps_pspnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PRPS','STORT',1,'proj_loc_proj');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','CHECT',1,'check_num_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','HBKID',1,'payr_hbkid_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','RZAWE',1,'payr_rzawe_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','ZALDT',1,'pymt_dt_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','ZBUKR',1,'payr_zbukr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','BELNR',1,'pymt_doc_num_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','BUKRS',1,'regup_bukrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','BUZEI',1,'regup_buzei_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','EBELN',1,'regup_ebeln_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','EBELP',1,'regup_ebelp_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','EMPFG',1,'payee_code_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','GJAHR',1,'regup_gjahr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','HKONT',1,'regup_hkont_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','KUNNR',1,'cx_num_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','LAUFD',1,'regup_laufd_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','LAUFI',1,'regup_laufi_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','LIFNR',1,'regup_lifnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','SAKNR',1,'regup_saknr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','VBLNR',1,'regup_vblnr_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','XVORL',1,'regup_xvorl_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','ZBUKR',1,'co_code_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','ZLSCH',1,'regup_zlsch_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T042ZT','LAND1',1,'t042zt_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T042ZT','SPRAS',1,'t042zt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T042ZT','TEXT2',1,'pymt_method_pmt');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T042ZT','ZLSCH',1,'t042zt_zlsch_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('J_1ATODCT','J_1ATODCT',1,'j_1atodct_j_1atodct_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('J_1ATODCT','SPRAS',1,'j_1atodct_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('J_1ATODCT','TEXT30',1,'tx_type_descr_tx');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T005S','BLAND',1,'t005s_bland_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T005S','FPRCD',1,'prov_tx_code_tx');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T005S','LAND1',1,'t005s_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007A','KALSM',1,'t007a_kalsm_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007A','MWSKZ',1,'t007a_mwskz_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','KALSM',1,'t007s_kalsm_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','MWSKZ',1,'t007s_mwskz_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','SPRAS',1,'t007s_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','TEXT1',1,'tx_name_tx');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TTXJT','KALSM',1,'ttxjt_kalsm_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TTXJT','SPRAS',1,'ttxjt_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TTXJT','TEXT1',1,'tx_jur_descr_tx');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TTXJT','TXJCD',1,'ttxjt_txjcd_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','BUKRS',1,'t001_bukrs_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','BUTXT',1,'co_name');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','LAND1',1,'t001_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001W','NAME1',1,'plant_name_plant');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001W','TXJCD',1,'plant_tx_jur_plant');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001W','WERKS',1,'t001w_werks_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T005T','LAND1',1,'t005t_land1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T005T','LANDX',1,'cntry_name');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T005T','SPRAS',1,'t005t_spras_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TINCT','BEZEI',1,'incoterms1_descr');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TINCT','INCO1',1,'tinct_inco1_key');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('TINCT','SPRAS',1,'tinct_spras_key');


"
