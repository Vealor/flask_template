#!/bin/bash

PGPASSWORD=LHDEV1234 psql -h localhost -U itra itra_db -c "
  INSERT INTO CLIENT_MODELS (client_id, hyper_p, pickle,train_data_start,train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','','2017-01-01','2018-01-01','inactive');
  INSERT INTO CLIENT_MODELS (client_id, hyper_p, pickle,train_data_start,train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','','2018-01-01','2019-01-01','inactive');
  INSERT INTO CLIENT_MODELS (client_id, hyper_p, pickle,train_data_start,train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','','2018-06-01','2019-06-01','active');
  INSERT INTO CLIENT_MODELS (client_id, hyper_p, pickle,train_data_start,train_data_end, status) VALUES (1, '{\"target\": \"\", \"predictors\": []}','','2018-06-01','2019-08-01','pending');

  INSERT INTO CLIENT_MODELS (client_id, hyper_p, pickle,train_data_start,train_data_end, status) VALUES (2, '{\"target\": \"\", \"predictors\": []}','','2018-01-01','2019-01-01','inactive');
  INSERT INTO CLIENT_MODELS (client_id, hyper_p, pickle,train_data_start,train_data_end, status) VALUES (2, '{\"target\": \"\", \"predictors\": []}','','2018-06-01','2019-06-01','active');

  INSERT INTO MASTER_MODELS (hyper_p, pickle, train_data_start,train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}','','2017-01-01','2018-01-01','inactive');
  INSERT INTO MASTER_MODELS (hyper_p, pickle, train_data_start,train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}', '','2018-01-01','2019-01-01','inactive');
  INSERT INTO MASTER_MODELS (hyper_p, pickle, train_data_start,train_data_end, status) VALUES ('{\"target\": \"\", \"predictors\": []}', '','2018-06-01','2019-06-01','active');
"
