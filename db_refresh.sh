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
FLASK_ENV='development'
flask db upgrade

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
    insert into line_of_business (name) values ('Business Services');
    insert into line_of_business (name) values ('Consumer & Retail');
    insert into line_of_business (name) values ('Energy & Natural Resources');
    insert into line_of_business (name) values ('Financial Services');
    insert into line_of_business (name) values ('Industrial Markets');
    insert into line_of_business (name) values ('Infrastructure, Government & Healthcare');
    insert into line_of_business (name) values ('Real Estate');
    insert into line_of_business (name) values ('Technology, Media & Telecommunication');

    insert into sectors (name, line_of_business_id) values ('Business Services', 1);
    insert into sectors (name, line_of_business_id) values ('Consumer Goods', 2);
    insert into sectors (name, line_of_business_id) values ('Food & Beverage', 2);
    insert into sectors (name, line_of_business_id) values ('Retail', 2);
    insert into sectors (name, line_of_business_id) values ('Forestry', 3);
    insert into sectors (name, line_of_business_id) values ('Mining', 3);
    insert into sectors (name, line_of_business_id) values ('Oil & Gas - Upstream', 3);
    insert into sectors (name, line_of_business_id) values ('Oil & Gas - Midstream', 3);
    insert into sectors (name, line_of_business_id) values ('Oil & Gas - Downstream', 3);
    insert into sectors (name, line_of_business_id) values ('Power & Utilities', 3);
    insert into sectors (name, line_of_business_id) values ('Asset Management', 4);
    insert into sectors (name, line_of_business_id) values ('Banking', 4);
    insert into sectors (name, line_of_business_id) values ('Insurance', 4);
    insert into sectors (name, line_of_business_id) values ('Pensions', 4);
    insert into sectors (name, line_of_business_id) values ('Private Equity', 4);
    insert into sectors (name, line_of_business_id) values ('Automotive', 5);
    insert into sectors (name, line_of_business_id) values ('Chemicals', 5);
    insert into sectors (name, line_of_business_id) values ('Industrial Mfg', 5);
    insert into sectors (name, line_of_business_id) values ('Aerospace & Defense', 6);
    insert into sectors (name, line_of_business_id) values ('Government Services', 6);
    insert into sectors (name, line_of_business_id) values ('Health & Life Science', 6);
    insert into sectors (name, line_of_business_id) values ('Transport & Infrastre', 6);
    insert into sectors (name, line_of_business_id) values ('Building & Construct', 7);
    insert into sectors (name, line_of_business_id) values ('Developers', 7);
    insert into sectors (name, line_of_business_id) values ('Hotels & Recreation', 7);
    insert into sectors (name, line_of_business_id) values ('Investors & Operator', 7);
    insert into sectors (name, line_of_business_id) values ('Media', 8);
    insert into sectors (name, line_of_business_id) values ('Technology', 8);
    insert into sectors (name, line_of_business_id) values ('Telecommunications', 8);

    insert into clients (name, line_of_business_id) values ('mining corp', 1);
    insert into clients (name, line_of_business_id) values ('mining corp two', 1);
    insert into clients (name, line_of_business_id) values ('mining corp', 2);
    insert into projects (name, client_id, juristiction) values ('miner 49er', 1, 'bc');
    insert into projects (name, client_id, juristiction) values ('miner 49er two', 1, 'ab');
    insert into projects (name, client_id, juristiction) values ('miner 50er', 2, 'sk');
    insert into projects (name, client_id, juristiction) values ('miner 51er', 3, 'foreign');
    insert into vendors (name) values ('miner buyer');
    insert into transactions(data, vendor_id, project_id) values ('{}', 1, 1);
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
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('order_no','PO Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('obj_key','Company Code','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('ref_procedure','Currency','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('doc_no','Document Header Text','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('document_header_text','ERP Document Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('doc_type','ERP Document Type','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('transaction_type','Fiscal Period','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('posting_date','Fiscal Year','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('company_code','Flag for Reversal','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('fiscal_year','FX Rate','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('ex_rate','Invoice Date','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('fiscal_period','Invoice Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('reverse_document_number_flag_for_credit','Posting Date','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('transaction_code','Reference Key','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('currency','Reference Transaction','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('entry_date','Cash Discount Percentage 1','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('clr_date','Amount in Document CCY','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('invoice_date','Amount in Local CCY','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('accounting_doc_line_no','Assignment Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('valuation_type','Billing Document','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('amount_in_local_currency','BSEG_Text Item','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('functional_area','Clearing Date','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('locationarea_of_business_description','Document Description','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('tax_code','Entry Date','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('network_no_for_acct_assgnmt','Functional Area','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('profit_ctr','GL Plant Name','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('wbs_element','Link for Payment Method','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('item_txt','Location/Area of Business Description','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('tax_jurisdiction','Network Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('sales_doc','Profit Center','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('billing_doc','Sales Document','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('plant_name','Task list number for operations in order','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('amount_in_document_currency','Tax Code','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('invoice_no','Tax Jurisdiction','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('link_for_payment_method','Transaction Type','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('assignment_no','Valuation Area','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('task_list_no_for_ops','Valuation Type','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('valuation_area','WBS Element Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('profit_ctr_name','General Name','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_dept','Controlling Area','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('control_area','Cost Center - Department','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_category','Cost Center Category','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_region','Person Responsible','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_tax_jur','Region (State, Province, County)','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_responsible_person','Tax Jurisdiction','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_description','Cost Center','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_valid_date','Description','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cost_centre_code','Search term for matchcode use','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('cc_name','Valid To Date','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('po_no','Item Number of Purchasing Document','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('po_line_no','PO Item Description','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('po_item_desc','PO Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('vendor_country','Vendor City','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('vendor_id','Vendor Country','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('vendor_name','Vendor Master_Vendor''s Phone Number 1','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('vendor_city','Vendor Master_Vendor''s Phone Number 2','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('vendor_province','Vendor Name','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('vendor_vat_no','Vendor Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('material_description','Material Description','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('material_no','Material Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('material_group','Material Group','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('payment_method','Amount Paid in the Payment Currency','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('payment_date','Check number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('document_number_of_the_payment_document','???','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('paying_company_code','Document Number of the Payment Document','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('pymt_method','Paying company code','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('pymt_term','???','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('chart_of_accounts','Account Name','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('acct_code','Account Number','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('acct_desc','Chart of Accounts','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('tax_key','Plant Region','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO cdm_labels(script_labels,english_labels,is_calculated,is_required,is_unique,datatype,regex) VALUES ('tax_code_description','Plant_Tax Jur','FALSE','TRUE','FALSE','dt_varchar','.*');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('AUFK','AUFNR',1,'order_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','AWKEY',1,'obj_key');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','AWTYP',1,'ref_procedure');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BELNR',1,'doc_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BKTXT',1,'document_header_text');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BLART',1,'doc_type');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BEWAR',1,'transaction_type');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BUDAT',1,'posting_date');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','BUKRS',1,'company_code');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','GJAHR',1,'fiscal_year');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','KURSF',1,'ex_rate');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','MONAT',1,'fiscal_period');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','STBLG',1,'reverse_document_number_flag_for_credit');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','TCODE',1,'transaction_code');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BKPF','WAERS',1,'currency');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','AUGBL',1,'entry_date');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','AUGDT',1,'clr_date');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BLDAT',1,'invoice_date');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BUZEI',1,'accounting_doc_line_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BWTAR',1,'valuation_type');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','DMBTR',1,'amount_in_local_currency');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','FKBER',1,'functional_area');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','GSBER',1,'locationarea_of_business_description');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','MWSK1',1,'tax_code');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','NPLNR',1,'network_no_for_acct_assgnmt');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','PRCTR',1,'profit_ctr');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','PROJK',1,'wbs_element');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','SGTXT',1,'item_txt');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','TXJCD',1,'tax_jurisdiction');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','VBEL2',1,'sales_doc');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','VBELN',1,'billing_doc');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','WERKS',1,'plant_name');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','WRBTR',1,'amount_in_document_currency');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','XBLNR',1,'invoice_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','ZLSCH',1,'link_for_payment_method');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','ZUONR',1,'assignment_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','AUFPL',1,'task_list_no_for_ops');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('BSEG','BWKEY',1,'valuation_area');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CEPCT','KTEXT',1,'profit_ctr_name');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','ABTEI',1,'cc_dept');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','KOKRS',1,'control_area');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','KOSAR',1,'cc_category');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','REGIO',1,'cc_region');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','TXJCD',1,'cc_tax_jur');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKS','VERAK',1,'cc_responsible_person');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','LTEXT',1,'cc_description');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','DATBI',1,'cc_valid_date');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KOSTL',1,'cost_centre_code');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('CSKT','KTEXT',1,'cc_name');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EBELN',1,'po_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','EBELP',1,'po_line_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('EKPO','TXZ01',1,'po_item_desc');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','LAND1',1,'vendor_country');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','LIFNR',1,'vendor_id');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','NAME1',1,'vendor_name');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','ORT01',1,'vendor_city');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','REGIO',1,'vendor_province');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('LFA1','STCEG',1,'vendor_vat_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','MAKTX',1,'material_description');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MAKT','MATNR',1,'material_no');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('MARA','MAKTL',1,'material_group');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','RZAWE',1,'payment_method');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('PAYR','ZALDT',1,'payment_date');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','VBLNR',1,'document_number_of_the_payment_document');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','ZBUKR',1,'paying_company_code');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','ZLSCH',1,'pymt_method');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('REGUP','ZTERM',1,'pymt_term');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','KTOPL',1,'chart_of_accounts');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','SAKNR',1,'acct_code');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('SKAT','TXT50',1,'acct_desc');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','KALSM',1,'tax_key');
    INSERT INTO data_mappings(table_name,column_name,project_id,cdm_label_script_label) VALUES ('T007S','TEXT1',1,'tax_code_description');
    "
