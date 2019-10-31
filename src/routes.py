from flask import jsonify
from src import api

#===============================================================================
### Endpoint Imports

# General Endpoints
from src.endpoints.general import general
api.register_blueprint(general, url_prefix='/')

# Auth Endpoints
from src.endpoints.auth import auth
api.register_blueprint(auth, url_prefix='/auth')

# CapsGen Endpoints
from src.endpoints.caps_gen import caps_gen
api.register_blueprint(caps_gen, url_prefix='/caps_gen')

# Client Endpoints
from src.endpoints.clients import clients
api.register_blueprint(clients, url_prefix='/clients')

# ClientModel Endpoints
from src.endpoints.client_models import client_models
api.register_blueprint(client_models, url_prefix='/client_models')

# Client Vendor Master Endpoint
from src.endpoints.client_vendor_master import client_vendor_master
api.register_blueprint(client_vendor_master, url_prefix='/client_vendor_master')

# DataMapping Endpoints
from src.endpoints.data_mappings import data_mappings
api.register_blueprint(data_mappings, url_prefix='/data_mappings')

# ClientModel Endpoints
from src.endpoints.data_params import data_params
api.register_blueprint(data_params, url_prefix='/data_params')

# FXrates Endpoints
from src.endpoints.fxrates import fxrates
api.register_blueprint(fxrates, url_prefix='/fxrates')

# Gst Registration Endpoint
from src.endpoints.gst_registration import gst_registration
api.register_blueprint(gst_registration, url_prefix='/gst_registration')

# Jurisdiction Endpoints
from src.endpoints.jurisdictions import jurisdictions
api.register_blueprint(jurisdictions, url_prefix='/jurisdictions')

# LineOfBusinessSectors Endpoints
from src.endpoints.lob_sectors import lob_sectors
api.register_blueprint(lob_sectors, url_prefix='/lob_sectors')

# Log Endpoints
from src.endpoints.logs import logs
api.register_blueprint(logs, url_prefix='/logs')

# MasterModel Endpoints
from src.endpoints.master_models import master_models
api.register_blueprint(master_models, url_prefix='/master_models')

# ParedownRule Endpoints
from src.endpoints.paredown_rules import paredown_rules
api.register_blueprint(paredown_rules, url_prefix='/paredown_rules')

# Project Endpoints
from src.endpoints.projects import projects
api.register_blueprint(projects, url_prefix='/projects')

# Tax Rate Endpoint
from src.endpoints.tax_rates import tax_rates
api.register_blueprint(tax_rates, url_prefix='/tax_rates')

# Transaction Endpoints
from src.endpoints.transactions import transactions
api.register_blueprint(transactions, url_prefix='/transactions')

# User Endpoints
from src.endpoints.users import users
api.register_blueprint(users, url_prefix='/users')

# Vendor Endpoints
from src.endpoints.vendors import vendors
api.register_blueprint(vendors, url_prefix='/vendors')


#===============================================================================
# Error Handling

# Bad Request
@api.errorhandler(400)
def _handle_endpoint_error(e):
    response = { 'status': 'Error 400', 'payload': [], 'message': e.description}
    return jsonify(response), 400
# Unauthorized
@api.errorhandler(401)
def _handle_endpoint_error(e):
    response = { 'status': 'Error 401', 'payload': [], 'message': e.description}
    return jsonify(response), 401
# Forbidden
@api.errorhandler(403)
def _handle_endpoint_error(e):
    response = { 'status': 'Error 403', 'payload': [], 'message': e.description}
    return jsonify(response), 403
# Not Found
@api.errorhandler(404)
def _handle_endpoint_error(e):
    response = { 'status': 'Error 404', 'payload': [], 'message': e.description}
    return jsonify(response), 404
# Method Not Allowed
@api.errorhandler(405)
def _handle_endpoint_error(e):
    response = { 'status': 'Error 405', 'payload': [], 'message': e.description}
    return jsonify(response), 405
# Unprocessable Entity
@api.errorhandler(422)
def _handle_endpoint_error(e):
    response = { 'status': 'Error 422', 'payload': [], 'message': e.description}
    return jsonify(response), 422
# Server Error
@api.errorhandler(500)
def _handle_server_error(e):
    response = { 'status': 'Error 500', 'payload': [], 'message': e.description}#'500 Server Error:  Please contact an Administrator.'}
    return jsonify(response), 500
