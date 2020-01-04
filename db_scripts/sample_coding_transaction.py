import sys; sys.path.append("..")

# Set-up the application context"
import numpy as np
import pandas as pd
import pickle

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models import *
from src.util import *
from src.prediction import model_client as cpm
from src.prediction import preprocessing as prepr

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()

def progress(count, total, status=''):
    bar_len = 30
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

if __name__ == '__main__':

    query = Transaction.query

    negative, positive = 201, 101
    trans_codes = [positive if float(tr.data['ap_amt']) > -10000 and tr.data['ccy'] != 'CAD' else negative for tr in query]
    l = len(trans_codes)
    approv_user = [1 if r < 0.8 else None for r in np.random.random(l)]

    # This is very slow, keep a progress bar
    c = 0
    for (tr,co,au,ii) in zip(query.all(), trans_codes, approv_user, range(l)):
        tr.modified = (datetime.datetime.now() - datetime.timedelta(days=np.round(1.0*(l - ii)*1000/l))).strftime("%Y-%m-%d_%H:%M:%S"),
        tr.update_codes([co],'gst_hst')
        tr.gst_hst_signed_off_by_id = 2
        tr.approved_user_id = au
        progress(ii, l, 'Updating Transaction data' )

    proj = Project.find_by_id(15)
    proj.has_ts_gst_hst = True
    #proj.has_ts_hst = True

    db.session.commit()

    # Now insert a pretrained predictive models for master and client.
    # print("Gathering Data..")
    # train_start = get_date_obj_from_str("2000-01-01")
    # train_end = get_date_obj_from_str('2018-12-31')
    # test_start = get_date_obj_from_str("2019-01-01")
    # test_end = get_date_obj_from_str('2019-08-01')
    #train_transactions = Transaction.query.filter(Transaction.modified.between(train_start,train_end)).filter(Transaction.approved_user_id != None)
    #test_transactions = Transaction.query.filter(Transaction.modified.between(test_start,test_end)).filter(Transaction.approved_user_id != None)
    #data_train = prepr.transactions_to_dataframe(train_transactions)
    #data_valid = prepr.transactions_to_dataframe(test_transactions)

    #df_train = prepr.preprocess_data(data_train,preprocess_for='training')
    # print("Training client model!")
    #m = cpm.ClientPredictionModel()
    #target = "Target"
    #predictors = list(set(df_train.columns) - set([target]))
    #m.train(df_train,predictors,target)

    # model_data_dict = {
    #         'client_id': 1,
    #         'train_data_start': train_start,
    #         'train_data_end': train_end,
    #         'pickle': pickle.dumps(None),
    #         'hyper_p': {'predictors': [], 'target': "Target"}
    #     }
    # entry = ClientModel(**model_data_dict)
    # entry.status = Activity.active
    # db.session.add(entry)
    # db.session.commit()
    # model_id = entry.id

    #df_valid = prepr.preprocess_data(data_valid,preprocess_for='validation',predictors=predictors)
    #performance_metrics = m.validate(df_valid, predictors, target)
    # model_performance_dict = {
    #     'accuracy': 0.76453543,
    #     'precision': 0.451991239,
    #     'recall': 0.9509423490,
    #     'test_data_start': test_start,
    #     'test_data_end': test_end
    # }
    #
    # # Push trained model and performance metrics
    # model_performance_dict['client_model_id'] = model_id
    # new_model_perf = ClientModelPerformance(**model_performance_dict)
    # db.session.add(new_model_perf)
    # db.session.commit()
