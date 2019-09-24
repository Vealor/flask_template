#!/usr/bin/env bash
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

read -n 1 -s -r -p "START SERVER NOW >> Press any key to continue when started"

curl -H "Content-Type: application/json" -X POST   -d '{
  "role":"it_admin",
  "username":"test",
  "password":"test",
  "special_token":"lhsuperamazingawesometoken",
  "email":"lh_test_user@kpmg.ca",
  "initials":"TEST",
  "first_name":"test_first",
  "last_name":"test_last"}' http://localhost:5000/auth/createadminsuperuseraccount
psql -h localhost -U itra itra_db -c "
  insert into logs (action, affected_entity, details, user_id) values('create', 'everything', 'such detail', 1);

  insert into clients (name) values ('mining corp');
  insert into clients (name) values ('mining corp two');
  insert into clients (name) values ('mining corp');
  insert into client_entities (client_id, company_code, lob_sector) values (1, '78GK', 'consumer_retail_food_beverage');
  insert into client_entity_jurisdictions (client_entity_id, jurisdiction) values (1, 'bc');
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 49er', 1, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 49er two', 1, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 50er', 2, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 51er', 3, 1, 1);
  insert into vendors (name) values ('miner buyer');
  insert into transactions (data, vendor_id, project_id) values ('{}', 1, 1);
  insert into user_project (user_id, project_id) values (1, 1);

INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BUKRS','BKPF_BUKRS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BELNR','BKPF_BELNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_GJAHR','BKPF_GJAHR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_XBLNR','BKPF_XBLNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BLDAT','BKPF_BLDAT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_BLART','BKPF_BLART','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_MONAT','BKPF_MONAT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_CPUTM','BKPF_CPUTM','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BKPF_KURSF','BKPF_KURSF','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_BUKRS','BSEG_BUKRS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_BELNR','BSEG_BELNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_GJAHR','BSEG_GJAHR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_LIFNR','BSEG_LIFNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_KOART','BSEG_KOART','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_EBELN','BSEG_EBELN','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_EBELP','BSEG_EBELP','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_KOSTL','BSEG_KOSTL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('BSEG_MWSKZ','BSEG_MWSKZ','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('CSKT_SPRAS','CSKT_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('CSKT_KTEXT','CSKT_KTEXT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('CSKT_KOSTL','CSKT_KOSTL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_EBELN','EKPO_EBELN','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_EBELP','EKPO_EBELP','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_MATNR','EKPO_MATNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('EKPO_TXZ01','EKPO_TXZ01','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_SPRAS','LFA1_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_LIFNR','LFA1_LIFNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_PSTLZ','LFA1_PSTLZ','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_STRAS','LFA1_STRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_LAND1','LFA1_LAND1','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_REGIO','LFA1_REGIO','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_ORT01','LFA1_ORT01','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_NAME1','LFA1_NAME1','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('LFA1_NAME2','LFA1_NAME2','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('MAKT_MAKTX','MAKT_MAKTX','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('MAKT_SPRAS','MAKT_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('MAKT_MATNR','MAKT_MATNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('PAYR_ZBUKR','PAYR_ZBUKR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('PAYR_VBLNR','PAYR_VBLNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('PAYR_GJAHR','PAYR_GJAHR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_SPRAS','SKAT_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_KTOPL','SKAT_KTOPL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_SAKNR','SKAT_SAKNR','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('SKAT_TXT50','SKAT_TXT50','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_SPRAS','T001_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_BUKRS','T001_BUKRS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_BUTXT','T001_BUTXT','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_WAERS','T001_WAERS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T001_KTOPL','T001_KTOPL','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_KALSM','T007S_KALSM','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_SPRAS','T007S_SPRAS','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_MWSKZ','T007S_MWSKZ','FALSE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('T007S_TEXT1','T007S_TEXT1','FALSE','TRUE','FALSE','dt_varchar','.*');
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
