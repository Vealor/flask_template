import sys; sys.path.append("..")

# Set-up the application context"

import numpy as np
import pandas as pd

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models import *
from src.util import *
from src.prediction import model_master_experiment as mpm_e
from src.prediction import model_master as mpm
from src.prediction import model_client as cpm
from src.prediction import preprocessing as prepr

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
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
    
    print("HERE!")
    negative, positive = 201, 101
    trans_codes = [positive if tr.data['cntry_name'] != 'Canada' and float(tr.data['ap_amt']) > -15000 else negative for tr in query]
    l = len(trans_codes)
    approv_user = [1 if r < 0.8 else None for r in np.random.random(l)]

    # This is very slow

    print("THERE!")
    c = 0
    for (tr,co,au,ii) in zip(query.all(),trans_codes, approv_user,range(l)):
        tr.modified = (datetime.datetime.now() - datetime.timedelta(days=np.round(1.0*(l - ii)*1000/l))).strftime("%Y-%m-%d_%H:%M:%S"),
        tr.update_gst_codes([co])
        tr.update_hst_codes([co])
        tr.gst_signed_off_by_id = 2
        tr.hst_signed_off_by_id = 3
        tr.approved_user_id = au
        progress(ii, l, 'Updating Transaction data' )

    print("..AND EVERYWHERE!")
    proj = Project.find_by_id(1)
    proj.has_ts_gst = True
    proj.has_ts_hst = True
        
    db.session.commit()