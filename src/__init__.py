'''
Main API Server
'''
#===============================================================================
from flask import Flask, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from pytz import timezone
from src.models import db
from src.util import *
#===============================================================================
# API Creation & Configuration
def build_api():
    api_build = Flask(__name__)
    CORS(api, supports_credentials=True)

    if api_build.config['ENV'] == 'development':
        print(bcolours.OKGREEN + "\n %% DEV %% \n"+ bcolours.ENDC)
        api_build.config.from_object('config.DevelopmentConfig')
    elif api_build.config['ENV'] == 'testing':
        print(bcolours.WARNING + "\n %% TEST %% \n"+ bcolours.ENDC)
        api_build.config.from_object('config.TestingConfig')
    elif api_build.config['ENV'] == 'production':
        print(bcolours.OKBLUE + "\n %% PROD %% \n"+ bcolours.ENDC)
        api_build.config.from_object('config.ProductionConfig')
    else:
        raise RuntimeError('CONFIGURATION STARTUP ERROR')

    api_build.url_map.strict_slashes = False
    return api_build

api = build_api()

db.init_app(api)
migrate = Migrate(api, db)
jwt = JWTManager(api)

#===============================================================================
# JWT helpers
from src import jwt_helpers
# Routing
from src import routes
