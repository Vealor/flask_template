#!/bin/bash

PGPASSWORD=$5 psql -h $1 -U $3 $4 -c "
  insert into logs (action, affected_entity, details, user_id) values('create', 'everything', 'such detail', 1);
  insert into clients (name) values ('Mining Corporation');
  insert into clients (name) values ('Oil & Gas Corporation');
  insert into clients (name) values ('Consumer & Retail Corporation');
  insert into client_entities (client_id, company_code, lob_sector) values (1, '78GK', 'consumer_retail_food_beverage');
  insert into client_entity_jurisdictions (client_entity_id, jurisdiction) values (1, 'bc');
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('North Mining', 1, 1, 1);
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('South Mining', 1, 1, 1);
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('Pipeline Northwest', 2, 1, 1);
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('Production Line CA', 3, 1, 1);
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('Production Line USA', 3, 1, 1);
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('Retail Unit S', 3, 1, 1);
  insert into projects (name, client_id, lead_partner_id, lead_manager_id) values ('Retail Unit N', 3, 1, 1);
  insert into caps_gen (user_id, project_id, is_completed) values (1, 1, True);
  insert into caps_gen (user_id, project_id, is_completed) values (1, 1, True);
  insert into fx_rates (date, usdtocad) values ('2010-01-01', 1.56);
  insert into fx_rates (date, usdtocad) values ('2010-01-02', 1.57);
  insert into transactions (data, project_id) values ('{}', 1);
  insert into transactions (data, project_id) values ('{}', 1);
  insert into transactions (data, project_id) values ('{}', 1);
  insert into transactions (data, project_id) values ('{}', 1);
  insert into transactions (data, project_id) values ('{}', 1);
  insert into transactions (data, project_id) values ('{}', 1);
  insert into transactions (data, project_id) values ('{}', 2);
  insert into transactions (data, project_id) values ('{}', 2);
  insert into transactions (data, project_id) values ('{}', 3);
  insert into transactions (data, project_id) values ('{}', 3);
  insert into user_project (user_id, project_id) values (1, 1);
  insert into gst_registration(caps_gen_id) values (1);

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
"
