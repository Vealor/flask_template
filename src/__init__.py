'''
Main API Server
'''
#===============================================================================
from src.models import db
from flask import Flask, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from pytz import timezone
from src.util import *
#===============================================================================
# API Creation & Configuration
def build_api():
    api = Flask(__name__)
    CORS(api, supports_credentials=True)

    if api.config['ENV'] == 'development':
        print(bcolours.OKGREEN + "\n %% DEV %% \n"+ bcolours.ENDC)
        api.config.from_object('config.DevelopmentConfig')
    elif api.config['ENV'] == 'testing':
        print(bcolours.WARNING + "\n %% TEST %% \n"+ bcolours.ENDC)
        api.config.from_object('config.TestingConfig')
    elif api.config['ENV'] == 'production':
        print(bcolours.OKBLUE + "\n %% PROD %% \n"+ bcolours.ENDC)
        api.config.from_object('config.ProductionConfig')
    else:
        raise RuntimeError('CONFIGURATION STARTUP ERROR')

    api.url_map.strict_slashes = False
    return api

api = build_api()

db.init_app(api)
migrate = Migrate(api, db)
jwt = JWTManager(api)

#===============================================================================
# JWT helpers
from src import jwt_helpers
# Routing
from src import routes
