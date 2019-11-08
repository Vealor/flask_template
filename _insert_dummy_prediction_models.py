import pickle
import sys; sys.path.append("../..")

# Set-up the application context
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models import *
from src.prediction import model_master as mpm
from src.prediction import model_client as cpm
from src.prediction.preprocessing import *


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()

hyper_p = [{"predictors": [], "target": "Target"}]

model_data_dict = {
    'train_data_start': "2019-01-01",
    'train_data_end': "2019-01-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'client_id': 1,
    'status': "active"
}
entry = ClientModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

model_data_dict = {
    'train_data_start': "2019-02-01",
    'train_data_end': "2019-02-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'client_id': 1,
    'status': "pending"
}
entry = ClientModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

model_data_dict = {
    'train_data_start': "2019-02-01",
    'train_data_end': "2019-04-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'client_id': 2,
    'status': "active"
}
entry = ClientModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

model_data_dict = {
    'train_data_start': "2018-02-01",
    'train_data_end': "2019-04-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'status': "active"
}
entry = MasterModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

model_data_dict = {
    'train_data_start': "2018-03-01",
    'train_data_end': "2019-05-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'status': "pending"
}
entry = MasterModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

model_data_dict = {
    'train_data_start': "2016-03-01",
    'train_data_end': "2017-05-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'status': "inactive"
}
entry = MasterModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

model_data_dict = {
    'train_data_start': "2017-03-01",
    'train_data_end': "2018-05-02",
    'pickle': pickle.dumps(None),
    'hyper_p': hyper_p,
    'status': "inactive"
}
entry = MasterModel(**model_data_dict)
db.session.add(entry)
db.session.flush()

db.session.commit()
