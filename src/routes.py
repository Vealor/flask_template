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

# Client Endpoints
from src.endpoints.clients import clients
api.register_blueprint(clients, url_prefix='/clients')

# Log Endpoints
from src.endpoints.logs import logs
api.register_blueprint(logs, url_prefix='/logs')

# Project Endpoints
from src.endpoints.projects import projects
api.register_blueprint(projects, url_prefix='/projects')

# Vendor Endpoints
from src.endpoints.vendors import vendors
api.register_blueprint(vendors, url_prefix='/vendors')

# Train Endpoints
from src.endpoints.train import train
api.register_blueprint(train, url_prefix='/train')

# Predict Endpoints
from src.endpoints.predict import predict
api.register_blueprint(predict, url_prefix='/predict')

#===============================================================================
# Error Handling

# Bad Request
@api.errorhandler(400)
def _handle_endpoint_error(e):
    response = { 'status': 'error 400', 'payload': [], 'message': str(e)}
    return jsonify(response), 400
# Unauthorized
@api.errorhandler(401)
def _handle_endpoint_error(e):
    response = { 'status': 'error 401', 'payload': [], 'message': str(e)}
    return jsonify(response), 401
# Forbidden
@api.errorhandler(403)
def _handle_endpoint_error(e):
    response = { 'status': 'error 403', 'payload': [], 'message': str(e)}
    return jsonify(response), 403
# Not Found
@api.errorhandler(404)
def _handle_endpoint_error(e):
    response = { 'status': 'error 404', 'payload': [], 'message': str(e)}
    return jsonify(response), 404
# Method Not Allowed
@api.errorhandler(405)
def _handle_endpoint_error(e):
    response = { 'status': 'error 405', 'payload': [], 'message': str(e)}
    return jsonify(response), 405
# Unprocessable Entity
@api.errorhandler(422)
def _handle_endpoint_error(e):
    response = { 'status': 'error 422', 'payload': [], 'message': str(e)}
    return jsonify(response), 422
# Server Error
@api.errorhandler(500)
def _handle_server_error(e):
    response = { 'status': 'error 500', 'payload': [], 'message': '500 Server Error:  Please contact an Administrator.'}
    return jsonify(response), 500
