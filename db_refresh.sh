#!/usr/bin/env bash

#!/usr/bin/env bash

sudo -i -u postgres psql <<EOF
drop database itra_db;
create database itra_db;
grant all privileges on database itra_db to itra;
EOF
source activate
FLASK_ENV='development' flask db upgrade 1c78a9dd073b

read -n 1 -s -r -p "START SERVER NOW >> Press any key to continue when started"
psql -h localhost -U itra itra_db -c "insert into industries (name) values ('mining'); insert into clients (name, industry_id) values ('mining corp', 1); insert into projects (name, client_id) values ('miner 49er', 1); insert into vendors (name) values ('miner buyer'); insert into transactions(data, vendor_id, project_id) values ('{}', 1, 1);"
flask db upgrade
psql -h localhost -U itra itra_db <<EOF
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','BUKRS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','KTOPL','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','BELNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','GJAHR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','XBLNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','BLDAT','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','BLART','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','MONAT','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','CPUTM','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BKPF','KURSF','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','BUKRS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','BELNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','GJAHR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','LIFNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','BLART','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','BLDAT','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','KOART','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','EBELN','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','EBELP','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','KOSTL','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('BSEG','MWSKZ','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('CSKT','SPRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('CSKT','KTEXT','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('CSKT','KOSTL','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('EKPO','EBELN','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('EKPO','EBELP','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('EKPO','MATNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('EKPO','TXZ01','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('EKPO','MATNR2','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','SPRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','LIFNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','PSTLZ','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','STRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','LAND1','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','REGIO','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','ORT01','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','NAME1','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('LFA1','NAME2','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('MAKT','MAKTX','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('MAKT','SPRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('MAKT','MATNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('PAYR','ZBUKR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('PAYR','VBLNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('PAYR','GJAHR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('SKAT','SPRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('SKAT','KTOPL','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('SKAT','SAKNR','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('SKAT','TXT50','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T001','SPRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T001','BUKRS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T001','BUTXT','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T001','WAERS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T001','TCODE','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T001','KTOPL','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T007','KALSM','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T007','SPRAS','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T007','MWSKZ','TRUE','FALSE','dt_varchar','.*');
INSERT INTO sap_linkingfields(table_name,field_name,is_complete,is_unique,datatype,regex) VALUES ('T007','TEXT1','TRUE','FALSE','dt_varchar','.*');
EOF
