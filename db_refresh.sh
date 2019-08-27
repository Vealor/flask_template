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
  insert into client_entities (client_id, company_code, lob_sector) values (1, 5892, 'consumer_retail_food_beverage');
  insert into client_entity_jurisdictions (client_entity_id, jurisdiction) values (1, 'bc');
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 49er', 1, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 49er two', 1, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 50er', 2, 1, 1);
  insert into projects (name, client_id, engagement_partner_id, engagement_manager_id) values ('miner 51er', 3, 1, 1);
  insert into vendors (name) values ('miner buyer');
  insert into transactions (data, vendor_id, project_id) values ('{}', 1, 1);
  insert into user_project (user_id, project_id) values (1, 1);
  "


##
