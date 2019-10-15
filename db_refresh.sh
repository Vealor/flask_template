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
  insert into fx_rates (date_id, usdtocad) values ('2010-01-01', 1.56);
  insert into fx_rates (date_id, usdtocad) values ('2010-01-02', 1.57);
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
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BUKRS','BKPF_BUKRS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BELNR','BKPF_BELNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_GJAHR','BKPF_GJAHR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_XBLNR','BKPF_XBLNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BLDAT','BKPF_BLDAT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BLART','BKPF_BLART','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_MONAT','BKPF_MONAT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_CPUTM','BKPF_CPUTM','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_KURSF','BKPF_KURSF','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_BUKRS','BSEG_BUKRS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_BELNR','BSEG_BELNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_GJAHR','BSEG_GJAHR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_LIFNR','BSEG_LIFNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_KOART','BSEG_KOART','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_EBELN','BSEG_EBELN','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_EBELP','BSEG_EBELP','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_KOSTL','BSEG_KOSTL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_MWSKZ','BSEG_MWSKZ','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('CSKT_SPRAS','CSKT_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('CSKT_KTEXT','CSKT_KTEXT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('CSKT_KOSTL','CSKT_KOSTL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_EBELN','EKPO_EBELN','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_EBELP','EKPO_EBELP','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_MATNR','EKPO_MATNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_TXZ01','EKPO_TXZ01','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_SPRAS','LFA1_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_LIFNR','LFA1_LIFNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_PSTLZ','LFA1_PSTLZ','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_STRAS','LFA1_STRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_LAND1','LFA1_LAND1','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_REGIO','LFA1_REGIO','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_ORT01','LFA1_ORT01','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_NAME1','LFA1_NAME1','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_NAME2','LFA1_NAME2','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('MAKT_MAKTX','MAKT_MAKTX','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('MAKT_SPRAS','MAKT_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('MAKT_MATNR','MAKT_MATNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('PAYR_ZBUKR','PAYR_ZBUKR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('PAYR_VBLNR','PAYR_VBLNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('PAYR_GJAHR','PAYR_GJAHR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_SPRAS','SKAT_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_KTOPL','SKAT_KTOPL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_SAKNR','SKAT_SAKNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_TXT50','SKAT_TXT50','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_SPRAS','T001_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_BUKRS','T001_BUKRS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_BUTXT','T001_BUTXT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_WAERS','T001_WAERS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_KTOPL','T001_KTOPL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_KALSM','T007S_KALSM','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_SPRAS','T007S_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_MWSKZ','T007S_MWSKZ','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_label,english_label,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_TEXT1','T007S_TEXT1','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BUKRS',1,'BKPF_BUKRS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BELNR',1,'BKPF_BELNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','GJAHR',1,'BKPF_GJAHR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','XBLNR',1,'BKPF_XBLNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BLDAT',1,'BKPF_BLDAT');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BLART',1,'BKPF_BLART');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','MONAT',1,'BKPF_MONAT');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','CPUTM',1,'BKPF_CPUTM');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','KURSF',1,'BKPF_KURSF');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BUKRS',1,'BSEG_BUKRS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BELNR',1,'BSEG_BELNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','GJAHR',1,'BSEG_GJAHR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','LIFNR',1,'BSEG_LIFNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','KOART',1,'BSEG_KOART');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','EBELN',1,'BSEG_EBELN');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','EBELP',1,'BSEG_EBELP');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','KOSTL',1,'BSEG_KOSTL');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MWSKZ',1,'BSEG_MWSKZ');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','SPRAS',1,'CSKT_SPRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KTEXT',1,'CSKT_KTEXT');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KOSTL',1,'CSKT_KOSTL');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EBELN',1,'EKPO_EBELN');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EBELP',1,'EKPO_EBELP');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','MATNR',1,'EKPO_MATNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','TXZ01',1,'EKPO_TXZ01');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','SPRAS',1,'LFA1_SPRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','LIFNR',1,'LFA1_LIFNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','PSTLZ',1,'LFA1_PSTLZ');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STRAS',1,'LFA1_STRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','LAND1',1,'LFA1_LAND1');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','REGIO',1,'LFA1_REGIO');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','ORT01',1,'LFA1_ORT01');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','NAME1',1,'LFA1_NAME1');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','NAME2',1,'LFA1_NAME2');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','MAKTX',1,'MAKT_MAKTX');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','SPRAS',1,'MAKT_SPRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','MATNR',1,'MAKT_MATNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','ZBUKR',1,'PAYR_ZBUKR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','VBLNR',1,'PAYR_VBLNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','GJAHR',1,'PAYR_GJAHR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','SPRAS',1,'SKAT_SPRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','KTOPL',1,'SKAT_KTOPL');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','SAKNR',1,'SKAT_SAKNR');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','TXT50',1,'SKAT_TXT50');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','SPRAS',1,'T001_SPRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','BUKRS',1,'T001_BUKRS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','BUTXT',1,'T001_BUTXT');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','WAERS',1,'T001_WAERS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T001','KTOPL',1,'T001_KTOPL');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','KALSM',1,'T007S_KALSM');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','SPRAS',1,'T007S_SPRAS');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','MWSKZ',1,'T007S_MWSKZ');
INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','TEXT1',1,'T007S_TEXT1');
"
