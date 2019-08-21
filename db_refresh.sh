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
  insert into projects (name, client_id, jurisdiction, engagement_partner_id, engagement_manager_id) values ('miner 49er', 1, 'bc', 1, 1);
  insert into projects (name, client_id, jurisdiction, engagement_partner_id, engagement_manager_id) values ('miner 49er two', 1, 'ab', 1, 1);
  insert into projects (name, client_id, jurisdiction, engagement_partner_id, engagement_manager_id) values ('miner 50er', 2, 'sk', 1, 1);
  insert into projects (name, client_id, jurisdiction, engagement_partner_id, engagement_manager_id) values ('miner 51er', 3, 'foreign', 1, 1);
  insert into vendors (name) values ('miner buyer');
  insert into transactions (data, vendor_id, project_id) values ('{}', 1, 1);
  insert into user_project (user_id, project_id) values (1, 1);
  "


##
