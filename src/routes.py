from flask import jsonify
from src import api

#===============================================================================
### Endpoint Imports

# General Endpoints (eg. Help & Error Handling)
from src.endpoints.general import general
api.register_blueprint(general, url_prefix='/')

# General Endpoints (eg. Help & Error Handling)
from src.endpoints.auth import auth
api.register_blueprint(auth, url_prefix='/auth')

#===============================================================================
# Error Handling
@api.errorhandler(400)
def _handle_endpoint_error(e):
    response = { 'status': 'error 400', 'payload': [], 'message': str(e)}
    return jsonify(response), 400
@api.errorhandler(401)
def _handle_endpoint_error(e):
    response = { 'status': 'error 401', 'payload': [], 'message': str(e)}
    return jsonify(response), 401
@api.errorhandler(403)
def _handle_endpoint_error(e):
    response = { 'status': 'error 403', 'payload': [], 'message': str(e)}
    return jsonify(response), 403
@api.errorhandler(404)
def _handle_endpoint_error(e):
    response = { 'status': 'error 404', 'payload': [], 'message': str(e)}
    return jsonify(response), 404
@api.errorhandler(405)
def _handle_endpoint_error(e):
    response = { 'status': 'error 405', 'payload': [], 'message': str(e)}
    return jsonify(response), 405
@api.errorhandler(422)
def _handle_endpoint_error(e):
    response = { 'status': 'error 422', 'payload': [], 'message': str(e)}
    return jsonify(response), 422
@api.errorhandler(500)
def _handle_server_error(e):
    response = { 'status': 'error 500', 'payload': [], 'message': '500 Server Error:  Please contact an Administrator.'}
    return jsonify(response), 500
