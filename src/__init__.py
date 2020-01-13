'''
Main API Server
'''
#===============================================================================
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.jwt_helpers import build_jwt_helpers
from src.models import db
from src.routes import build_blueprints
from src.util import bcolours
#===============================================================================
# API Creation & Configuration
def build_api():
    api_build = Flask(__name__)
    CORS(api_build, supports_credentials=True)
    api_build.url_map.strict_slashes = False  # critical to come before build_blueprints

    if api_build.config['ENV'] == 'development':
        print(bcolours.OKGREEN + "\n %% DEV %% \n" + bcolours.ENDC)
        api_build.config.from_object('config.DevelopmentConfig')
    elif api_build.config['ENV'] == 'testing':
        print(bcolours.WARNING + "\n %% TEST %% \n" + bcolours.ENDC)
        api_build.config.from_object('config.TestingConfig')
    elif api_build.config['ENV'] == 'production':
        print(bcolours.OKBLUE + "\n %% PROD %% \n" + bcolours.ENDC)
        api_build.config.from_object('config.ProductionConfig')
    else:
        raise RuntimeError('CONFIGURATION STARTUP ERROR')

    db.init_app(api_build)
    build_blueprints(api_build)
    build_jwt_helpers(JWTManager(api_build))
    Migrate(api_build, db)
    return api_build

api = build_api()
