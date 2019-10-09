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


  insert into paredown_rules (id) values (1);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (1, 'Acct_Desc', 'contains', 'Donation', 210);

  insert into paredown_rules (id) values (2);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (2, 'Item_Text', 'contains', 'Donation', 210);

  insert into paredown_rules (id) values (3);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (3, 'INVOICE_NUM', 'contains', 'Donation', 210);

  insert into paredown_rules (id) values (4);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (4, 'Acct_Desc', 'contains', 'Sponsorship', 210);

  insert into paredown_rules (id) values (5);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (5, 'Item_Text', 'contains', 'Sponsorship', 210);

  insert into paredown_rules (id) values (6);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (6, 'INVOICE_NUM', 'contains', 'Sponsorship', 210);

  insert into paredown_rules (id) values (7);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (7, 'Acct_Desc', 'contains', 'Charity', 210);

  insert into paredown_rules (id) values (8);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (8, 'Item_Text', 'contains', 'Charity', 210);

  insert into paredown_rules (id) values (9);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (9, 'INVOICE_NUM', 'contains', 'Charity', 210);

  insert into paredown_rules (id) values (10);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (10, 'Acct_Desc', 'contains', 'Insurance', 221, 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (10, 'VEND_EFF_RATE_N', '<', '1', 221, 'Insurance');

  insert into paredown_rules (id) values (11);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (11, 'Item_Text', 'contains', 'Insurance', 221, 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (11, 'VEND_EFF_RATE_N', '<', '1', 221, 'Insurance');

  insert into paredown_rules (id) values (12);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (12, 'INVOICE_NUM', 'contains', 'Insurance', 221, 'Insurance');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (12, 'VEND_EFF_RATE_N', '<', '1', 221, 'Insurance');

  insert into paredown_rules (id) values (13);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (13, 'Acct_Desc', 'contains', 'Health', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (13, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (14);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (14, 'Item_Text', 'contains', 'Health', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (14, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (15);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (15, 'INVOICE_NUM', 'contains', 'Health', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (15, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (16);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (16, 'Acct_Desc', 'contains', 'Dental', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (16, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (17);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (17, 'Item_Text', 'contains', 'Dental', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (17, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (18);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (18, 'INVOICE_NUM', 'contains', 'Dental', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (18, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (19);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (19, 'Acct_Desc', 'contains', 'Disability', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (19, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (20);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (20, 'Item_Text', 'contains', 'Disability', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (20, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (21);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (21, 'INVOICE_NUM', 'contains', 'Disability', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (21, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (22);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (22, 'Acct_Desc', 'contains', 'LTD', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (22, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (23);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (23, 'Item_Text', 'contains', 'LTD', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (23, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (24);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (24, 'INVOICE_NUM', 'contains', 'LTD', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (24, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (25);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (25, 'Acct_Desc', 'contains', 'STD', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (25, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (26);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (26, 'Item_Text', 'contains', 'STD', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (26, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (27);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (27, 'INVOICE_NUM', 'contains', 'STD', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (27, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (28);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (28, 'Acct_Desc', 'contains', 'Medical', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (28, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (29);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (29, 'Item_Text', 'contains', 'Medical', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (29, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (30);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (30, 'INVOICE_NUM', 'contains', 'Medical', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (30, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (31);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (31, 'Acct_Desc', 'contains', 'Medical Services Plan', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (31, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (32);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (32, 'Item_Text', 'contains', 'Medical Services Plan', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (32, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (33);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (33, 'Acct_Desc', 'contains', 'MSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (33, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (34);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (34, 'Item_Text', 'contains', 'MSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (34, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (35);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (35, 'INVOICE_NUM', 'contains', 'MSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (35, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (36);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (36, 'Acct_Desc', 'contains', 'Payroll', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (36, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (37);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (37, 'Item_Text', 'contains', 'Payroll', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (37, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (38);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (38, 'INVOICE_NUM', 'contains', 'Payroll', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (38, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (39);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (39, 'Acct_Desc', 'contains', 'Salary', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (39, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (40);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (40, 'Item_Text', 'contains', 'Salary', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (40, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (41);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (41, 'INVOICE_NUM', 'contains', 'Salary', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (41, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (42);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (42, 'Acct_Desc', 'contains', 'Salaries', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (42, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (43);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (43, 'Item_Text', 'contains', 'Salaries', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (43, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (44);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (44, 'INVOICE_NUM', 'contains', 'Salaries', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (44, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (45);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (45, 'Acct_Desc', 'contains', 'Severance', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (45, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (46);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (46, 'Item_Text', 'contains', 'Severance', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (46, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (47);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (47, 'INVOICE_NUM', 'contains', 'Severance', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (47, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (48);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (48, 'Acct_Desc', 'contains', 'Employment insurance', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (48, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (49);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (49, 'Item_Text', 'contains', 'Employment insurance', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (49, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (50);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (50, 'Acct_Desc', 'contains', 'Employer Health Tax', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (50, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (51);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (51, 'Item_Text', 'contains', 'Employer Health Tax', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (51, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (52);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (52, 'Acct_Desc', 'contains', 'EHT', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (52, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (53);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (53, 'Item_Text', 'contains', 'EHT', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (53, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (54);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (54, 'INVOICE_NUM', 'contains', 'EHT', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (54, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (55);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (55, 'Acct_Desc', 'contains', 'Garnish', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (55, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (56);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (56, 'Item_Text', 'contains', 'Garnish', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (56, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (57);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (57, 'INVOICE_NUM', 'contains', 'Garnish', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (57, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (58);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (58, 'Acct_Desc', 'contains', 'Share purchase', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (58, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (59);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (59, 'Item_Text', 'contains', 'Share purchase', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (59, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (60);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (60, 'Acct_Desc', 'contains', 'LTIP ', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (60, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (61);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (61, 'Item_Text', 'contains', 'LTIP ', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (61, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (62);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (62, 'INVOICE_NUM', 'contains', 'LTIP ', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (62, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (63);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (63, 'Acct_Desc', 'contains', 'RRSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (63, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (64);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (64, 'Item_Text', 'contains', 'RRSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (64, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (65);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (65, 'INVOICE_NUM', 'contains', 'RRSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (65, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (66);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (66, 'Acct_Desc', 'contains', 'Work Safety', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (66, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (67);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (67, 'Item_Text', 'contains', 'Work Safety', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (67, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (68);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (68, 'Acct_Desc', 'contains', 'Workers Comp', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (68, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (69);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (69, 'Item_Text', 'contains', 'Workers Comp', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (69, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (70);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (70, 'Acct_Desc', 'contains', 'workers compensation board', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (70, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (71);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (71, 'Item_Text', 'contains', 'workers compensation board', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (71, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (72);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (72, 'Acct_Desc', 'contains', 'Worksafe BC', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (72, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (73);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (73, 'Item_Text', 'contains', 'Worksafe BC', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (73, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (74);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (74, 'Acct_Desc', 'contains', 'WorksafeBC', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (74, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (75);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (75, 'Item_Text', 'contains', 'WorksafeBC', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (75, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (76);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (76, 'Acct_Desc', 'contains', 'BCMSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (76, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (77);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (77, 'Item_Text', 'contains', 'BCMSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (77, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (78);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (78, 'INVOICE_NUM', 'contains', 'BCMSP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (78, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (79);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (79, 'Acct_Desc', 'contains', 'WSIB', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (79, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (80);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (80, 'Item_Text', 'contains', 'WSIB', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (80, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (81);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (81, 'INVOICE_NUM', 'contains', 'WSIB', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (81, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (82);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (82, 'Acct_Desc', 'contains', 'Workplace Safety & Insurance Board', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (82, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (83);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (83, 'Item_Text', 'contains', 'Workplace Safety & Insurance Board', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (83, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (84);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (84, 'Acct_Desc', 'contains', 'Canada Pension Plan', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (84, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (85);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (85, 'Item_Text', 'contains', 'Canada Pension Plan', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (85, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (86);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (86, 'Acct_Desc', 'contains', 'WCB', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (86, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (87);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (87, 'Item_Text', 'contains', 'WCB', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (87, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (88);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (88, 'INVOICE_NUM', 'contains', 'WCB', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (88, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (89);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (89, 'Acct_Desc', 'contains', 'Union due', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (89, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (90);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (90, 'Item_Text', 'contains', 'Union due', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (90, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (91);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (91, 'Acct_Desc', 'contains', 'Pension', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (91, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (92);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (92, 'Item_Text', 'contains', 'Pension', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (92, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (93);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (93, 'INVOICE_NUM', 'contains', 'Pension', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (93, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (94);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (94, 'Acct_Desc', 'contains', 'Dividends', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (94, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (95);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (95, 'Item_Text', 'contains', 'Dividends', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (95, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (96);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (96, 'INVOICE_NUM', 'contains', 'Dividends', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (96, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (97);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (97, 'Acct_Desc', 'contains', 'EI ', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (97, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (98);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (98, 'Item_Text', 'contains', 'EI ', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (98, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (99);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (99, 'Acct_Desc', 'contains', 'CPP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (99, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (100);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (100, 'Item_Text', 'contains', 'CPP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (100, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (101);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (101, 'INVOICE_NUM', 'contains', 'CPP', 221, 'Payroll / Benefits');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (101, 'VEND_EFF_RATE_N', '<', '1', 221, 'Payroll / Benefits');

  insert into paredown_rules (id) values (102);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (102, 'Acct_Desc', 'contains', 'Loan', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (102, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (103);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (103, 'Item_Text', 'contains', 'Loan', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (103, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (104);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (104, 'INVOICE_NUM', 'contains', 'Loan', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (104, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (105);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (105, 'Acct_Desc', 'contains', 'Debt', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (105, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (106);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (106, 'Item_Text', 'contains', 'Debt', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (106, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (107);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (107, 'INVOICE_NUM', 'contains', 'Debt', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (107, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (108);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (108, 'Acct_Desc', 'contains', 'Interest', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (108, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (109);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (109, 'Item_Text', 'contains', 'Interest', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (109, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (110);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (110, 'INVOICE_NUM', 'contains', 'Interest', 209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (110, 'VEND_EFF_RATE_N', '<', '1', 209);

  insert into paredown_rules (id) values (111);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (111, 'Acct_Desc', 'contains', 'Toll', 221, 'Tolls');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (111, 'VEND_EFF_RATE_N', '<', '1', 221, 'Tolls');

  insert into paredown_rules (id) values (112);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (112, 'Item_Text', 'contains', 'Toll', 221, 'Tolls');
  insert into paredown_rules_conditions (rule_id, field, operator, value, code, comment) values (112, 'VEND_EFF_RATE_N', '<', '1', 221, 'Tolls');

  insert into paredown_rules (id) values (113);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (113, 'INVOICE_NUM', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (113, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (113, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (114);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (114, 'Acct_Desc', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (114, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (114, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (115);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (115, 'Item_Text', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (115, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (115, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (116);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (116, 'INVOICE_NUM', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (116, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (116, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (117);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (117, 'Acct_Desc', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (117, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (117, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (118);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (118, 'Item_Text', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (118, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (118, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (119);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (119, 'INVOICE_NUM', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (119, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (119, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (120);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (120, 'Acct_Desc', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (120, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (120, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (121);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (121, 'Item_Text', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (121, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (121, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (122);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (122, 'INVOICE_NUM', 'contains', 'CT ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (122, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (122, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (123);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (123, 'Acct_Desc', 'contains', 'CT ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (123, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (123, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (124);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (124, 'Item_Text', 'contains', 'CT ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (124, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (124, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (125);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (125, 'INVOICE_NUM', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (125, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (125, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (126);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (126, 'Acct_Desc', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (126, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (126, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (127);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (127, 'Item_Text', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (127, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (127, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (128);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (128, 'INVOICE_NUM', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (128, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (128, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (129);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (129, 'Acct_Desc', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (129, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (129, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (130);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (130, 'Item_Text', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (130, 'SUPPLIER_NAME', 'contains', 'Receiver General ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (130, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (131);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (131, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (131, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (131, 'Acct_Desc', 'contains', 'tax', 208);

  insert into paredown_rules (id) values (132);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (132, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (132, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (132, 'Item_Text', 'contains', 'tax', 208);

  insert into paredown_rules (id) values (133);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (133, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (133, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (133, 'INVOICE_NUM', 'contains', 'MFT', 208);

  insert into paredown_rules (id) values (134);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (134, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (134, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (134, 'Acct_Desc', 'contains', 'MFT', 208);

  insert into paredown_rules (id) values (135);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (135, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (135, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (135, 'Item_Text', 'contains', 'MFT', 208);

  insert into paredown_rules (id) values (136);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (136, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (136, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (136, 'INVOICE_NUM', 'contains', 'PST ', 208);

  insert into paredown_rules (id) values (137);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (137, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (137, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (137, 'Acct_Desc', 'contains', 'PST ', 208);

  insert into paredown_rules (id) values (138);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (138, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (138, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (138, 'Item_Text', 'contains', 'PST ', 208);

  insert into paredown_rules (id) values (139);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (139, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (139, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (139, 'INVOICE_NUM', 'contains', 'CT ', 208);

  insert into paredown_rules (id) values (140);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (140, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (140, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (140, 'Acct_Desc', 'contains', 'CT ', 208);

  insert into paredown_rules (id) values (141);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (141, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (141, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (141, 'Item_Text', 'contains', 'CT ', 208);

  insert into paredown_rules (id) values (142);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (142, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (142, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (142, 'INVOICE_NUM', 'contains', 'GST', 208);

  insert into paredown_rules (id) values (143);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (143, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (143, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (143, 'Acct_Desc', 'contains', 'GST', 208);

  insert into paredown_rules (id) values (144);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (144, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (144, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (144, 'Item_Text', 'contains', 'GST', 208);

  insert into paredown_rules (id) values (145);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (145, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (145, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (145, 'INVOICE_NUM', 'contains', 'QST', 208);

  insert into paredown_rules (id) values (146);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (146, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (146, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (146, 'Acct_Desc', 'contains', 'QST', 208);

  insert into paredown_rules (id) values (147);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (147, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (147, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (147, 'Item_Text', 'contains', 'QST', 208);

  insert into paredown_rules (id) values (148);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (148, 'SUPPLIER_NAME', 'contains', 'Ministry', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (148, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (148, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (149);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (149, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (149, 'Acct_Desc', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (149, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (150);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (150, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (150, 'Item_Text', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (150, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (151);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (151, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (151, 'INVOICE_NUM', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (151, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (152);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (152, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (152, 'Acct_Desc', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (152, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (153);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (153, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (153, 'Item_Text', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (153, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (154);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (154, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (154, 'INVOICE_NUM', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (154, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (155);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (155, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (155, 'Acct_Desc', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (155, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (156);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (156, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (156, 'Item_Text', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (156, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (157);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (157, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (157, 'INVOICE_NUM', 'contains', 'CT ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (157, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (158);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (158, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (158, 'Acct_Desc', 'contains', 'CT ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (158, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (159);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (159, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (159, 'Item_Text', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (159, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (160);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (160, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (160, 'INVOICE_NUM', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (160, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (161);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (161, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (161, 'Acct_Desc', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (161, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (162);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (162, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (162, 'Item_Text', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (162, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (163);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (163, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (163, 'INVOICE_NUM', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (163, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (164);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (164, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (164, 'Acct_Desc', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (164, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (165);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (165, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (165, 'Item_Text', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (165, 'SUPPLIER_NAME', 'contains', 'CRA', 208);

  insert into paredown_rules (id) values (166);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (166, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (166, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (166, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (167);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (167, 'Acct_Desc', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (167, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (167, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (168);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (168, 'Item_Text', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (168, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (168, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (169);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (169, 'INVOICE_NUM', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (169, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (169, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (170);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (170, 'Acct_Desc', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (170, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (170, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (171);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (171, 'Item_Text', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (171, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (171, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (172);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (172, 'INVOICE_NUM', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (172, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (172, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (173);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (173, 'Acct_Desc', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (173, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (173, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (174);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (174, 'Item_Text', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (174, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (174, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (175);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (175, 'INVOICE_NUM', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (175, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (175, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (176);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (176, 'Acct_Desc', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (176, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (176, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (177);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (177, 'Item_Text', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (177, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (177, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (178);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (178, 'INVOICE_NUM', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (178, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (178, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (179);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (179, 'Acct_Desc', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (179, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (179, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (180);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (180, 'Item_Text', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (180, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (180, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (181);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (181, 'INVOICE_NUM', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (181, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (181, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (182);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (182, 'Acct_Desc', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (182, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (182, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (183);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (183, 'Item_Text', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (183, 'SUPPLIER_NAME', 'contains', 'Canada Revenue', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (183, 'Acct_Desc', 'contains', 'AP amount', 208);

  insert into paredown_rules (id) values (184);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (184, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (184, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (184, 'Acct_Desc', 'contains', 'tax', 208);

  insert into paredown_rules (id) values (185);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (185, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (185, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (185, 'Item_Text', 'contains', 'tax', 208);

  insert into paredown_rules (id) values (186);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (186, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (186, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (186, 'INVOICE_NUM', 'contains', 'MFT', 208);

  insert into paredown_rules (id) values (187);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (187, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (187, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (187, 'Acct_Desc', 'contains', 'MFT', 208);

  insert into paredown_rules (id) values (188);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (188, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (188, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (188, 'Item_Text', 'contains', 'MFT', 208);

  insert into paredown_rules (id) values (189);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (189, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (189, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (189, 'INVOICE_NUM', 'contains', 'PST ', 208);

  insert into paredown_rules (id) values (190);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (190, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (190, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (190, 'Acct_Desc', 'contains', 'PST ', 208);

  insert into paredown_rules (id) values (191);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (191, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (191, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (191, 'Item_Text', 'contains', 'PST ', 208);

  insert into paredown_rules (id) values (192);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (192, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (192, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (192, 'INVOICE_NUM', 'contains', 'CT', 208);

  insert into paredown_rules (id) values (193);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (193, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (193, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (193, 'Acct_Desc', 'contains', 'CT', 208);

  insert into paredown_rules (id) values (194);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (194, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (194, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (194, 'Item_Text', 'contains', 'CT', 208);

  insert into paredown_rules (id) values (195);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (195, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (195, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (195, 'INVOICE_NUM', 'contains', 'GST', 208);

  insert into paredown_rules (id) values (196);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (196, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (196, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (196, 'Acct_Desc', 'contains', 'GST', 208);

  insert into paredown_rules (id) values (197);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (197, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (197, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (197, 'Item_Text', 'contains', 'GST', 208);

  insert into paredown_rules (id) values (198);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (198, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (198, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (198, 'INVOICE_NUM', 'contains', 'QST', 208);

  insert into paredown_rules (id) values (199);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (199, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (199, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (199, 'Acct_Desc', 'contains', 'QST', 208);

  insert into paredown_rules (id) values (200);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (200, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (200, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (200, 'Item_Text', 'contains', 'QST', 208);

  insert into paredown_rules (id) values (201);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (201, 'SUPPLIER_NAME', 'contains', 'Canada Customs', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (201, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (201, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (202);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (202, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (202, 'Acct_Desc', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (202, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (203);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (203, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (203, 'Item_Text', 'contains', 'tax', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (203, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (204);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (204, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (204, 'INVOICE_NUM', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (204, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (205);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (205, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (205, 'Acct_Desc', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (205, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (206);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (206, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (206, 'Item_Text', 'contains', 'MFT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (206, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (207);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (207, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (207, 'INVOICE_NUM', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (207, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (208, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (208, 'Acct_Desc', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (208, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (209);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (209, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (209, 'Item_Text', 'contains', 'PST ', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (209, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (210);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (210, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (210, 'INVOICE_NUM', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (210, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (211);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (211, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (211, 'Acct_Desc', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (211, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (212);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (212, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (212, 'Item_Text', 'contains', 'CT', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (212, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (213);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (213, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (213, 'INVOICE_NUM', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (213, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (214);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (214, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (214, 'Acct_Desc', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (214, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (215);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (215, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (215, 'Item_Text', 'contains', 'GST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (215, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (216);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (216, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (216, 'INVOICE_NUM', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (216, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (217);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (217, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (217, 'Acct_Desc', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (217, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (218);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (218, 'Acct_Desc', 'contains', 'AP amount', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (218, 'Item_Text', 'contains', 'QST', 208);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (218, 'SUPPLIER_NAME', 'contains', 'Revenue Quebec', 208);

  insert into paredown_rules (id) values (219);
  insert into paredown_rules_conditions (rule_id, field, operator, value, code) values (219, 'Acct_Desc', 'contains', 'AP amount', 208);
  "


##
