#!/bin/bash

#PGPASSWORD=$5 psql -h $1 -U $3 $4 -c "
PGPASSWORD=LHDEV1234 psql -h localhost -U itra itra_db -c "
  INSERT INTO client_models (client_id, hyper_p, pickle, train_data_start, train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2017-01-01','2018-01-01','inactive');
  INSERT INTO client_models (client_id, hyper_p, pickle, train_data_start, train_data_end, status) VALUES (2, '{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2017-01-01','2018-01-01','inactive');
  INSERT INTO client_models (client_id, hyper_p, pickle, train_data_start, train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2017-09-01','2018-09-01','inactive');
  INSERT INTO client_models (client_id, hyper_p, pickle, train_data_start, train_data_end, status) VALUES (2, '{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2018-06-01','2019-06-01','active');
  INSERT INTO client_models (client_id, hyper_p, pickle, train_data_start, train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2019-09-01','2018-09-01','active');
  INSERT INTO client_models (client_id, hyper_p, pickle, train_data_start, train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2018-06-01','2019-06-01','pending');

  INSERT INTO master_models (hyper_p, pickle, train_data_start, train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2017-01-01','2018-01-01','inactive');
  INSERT INTO master_models (hyper_p, pickle, train_data_start, train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2017-06-01','2018-06-01','inactive');
  INSERT INTO master_models (hyper_p, pickle, train_data_start, train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2019-09-01','2018-09-01','active');
  INSERT INTO master_models (hyper_p, pickle, train_data_start, train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}','\x8004950800000000000000430480034e2e942e','2018-06-01','2019-06-01','pending');
"
