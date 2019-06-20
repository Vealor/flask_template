'''
Main API Server
'''
#===============================================================================
from src.models import db, ma
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from pytz import timezone
#===============================================================================
# API Creation & Configuration
api = Flask(__name__) # global application initialization
CORS(api)
api.config.from_object('config')
api.url_map.strict_slashes = False
db.init_app(api)
ma.init_app(api)

from src import routes
