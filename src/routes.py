from flask import jsonify

#===============================================================================
### Endpoint Imports
def build_blueprints(api):
    # General Endpoints
    from src.endpoints.general import general  # noqa: E402
    api.register_blueprint(general, url_prefix='/')

    # Auth Endpoints
    from src.endpoints.auth import auth  # noqa: E402
    api.register_blueprint(auth, url_prefix='/auth')

    # Log Endpoints
    from src.endpoints.logs import logs  # noqa: E402
    api.register_blueprint(logs, url_prefix='/logs')

    # User Endpoints
    from src.endpoints.users import users  # noqa: E402
    api.register_blueprint(users, url_prefix='/users')

    #===============================================================================
    # Error Handling

    # Bad Request
    @api.errorhandler(400)
    def _handle_endpoint_error_400(err):
        response = {'status': 'Error 400', 'payload': [], 'message': err.description}
        return jsonify(response), 400

    # Unauthorized
    @api.errorhandler(401)
    def _handle_endpoint_error_401(err):
        response = {'status': 'Error 401', 'payload': [], 'message': err.description}
        return jsonify(response), 401

    # Forbidden
    @api.errorhandler(403)
    def _handle_endpoint_error_403(err):
        response = {'status': 'Error 403', 'payload': [], 'message': err.description}
        return jsonify(response), 403

    # Not Found
    @api.errorhandler(404)
    def _handle_endpoint_error_404(err):
        response = {'status': 'Error 404', 'payload': [], 'message': err.description}
        return jsonify(response), 404

    # Method Not Allowed
    @api.errorhandler(405)
    def _handle_endpoint_error_405(err):
        response = {'status': 'Error 405', 'payload': [], 'message': err.description}
        return jsonify(response), 405

    # Conflict
    @api.errorhandler(409)
    def _handle_endpoint_error_409(err):
        response = {'status': 'Error 409', 'payload': [], 'message': err.description}
        return jsonify(response), 409

    # Unprocessable Entity
    @api.errorhandler(422)
    def _handle_endpoint_error_422(err):
        response = {'status': 'Error 422', 'payload': [], 'message': err.description}
        return jsonify(response), 422

    # Server Error
    @api.errorhandler(500)
    def _handle_server_error_500(err):
        response = {'status': 'Error 500', 'payload': [], 'message': err.description}
        return jsonify(response), 500
