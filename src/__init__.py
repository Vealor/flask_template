'''
Main API Server
'''
#===============================================================================
from src.models import db, ma
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from pytz import timezone
#===============================================================================
# API Creation & Configuration
api = Flask(__name__) # global application initialization
CORS(api, supports_credentials=True)
api.config.from_object('config')
api.url_map.strict_slashes = False
db.init_app(api)
ma.init_app(api)
migrate = Migrate(api, db)
jwt = JWTManager(api)

# Check token blacklisting
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.BlacklistTokenModel.is_blacklisted(jti)

# TODO: https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/loaders.py

from src import routes
