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

    # CapsGen Endpoints
    from src.endpoints.caps_gen import caps_gen  # noqa: E402
    api.register_blueprint(caps_gen, url_prefix='/caps_gen')

    # CDMLabel Endpoints
    from src.endpoints.cdm_labels import cdm_labels  # noqa: E402
    api.register_blueprint(cdm_labels, url_prefix='/cdm_labels')

    # Client Endpoints
    from src.endpoints.clients import clients  # noqa: E402
    api.register_blueprint(clients, url_prefix='/clients')

    # ClientModel Endpoints
    from src.endpoints.client_models import client_models  # noqa: E402
    api.register_blueprint(client_models, url_prefix='/client_models')

    # Client Vendor Master Endpoint
    from src.endpoints.client_vendor_master import client_vendor_master  # noqa: E402
    api.register_blueprint(client_vendor_master, url_prefix='/client_vendor_master')

    # Client Tax GL Extract Endpoint
    from src.endpoints.client_tax_gl_extract import client_tax_gl_extract  # noqa: E402
    api.register_blueprint(client_tax_gl_extract, url_prefix='/client_tax_gl_extract')

    # Code Endpoint
    from src.endpoints.codes import codes  # noqa: E402
    api.register_blueprint(codes, url_prefix='/codes')

    # DataMapping Endpoints
    from src.endpoints.data_mappings import data_mappings  # noqa: E402
    api.register_blueprint(data_mappings, url_prefix='/data_mappings')

    # DataParam Endpoints
    from src.endpoints.data_params import data_params  # noqa: E402
    api.register_blueprint(data_params, url_prefix='/data_params')

    # ErrorCategory Endpoints
    from src.endpoints.error_categories import error_categories  # noqa: E402
    api.register_blueprint(error_categories, url_prefix='/error_categories')

    # FXrates Endpoints
    from src.endpoints.fx_rates import fx_rates  # noqa: E402
    api.register_blueprint(fx_rates, url_prefix='/fx_rates')

    # Gst Registration Endpoint
    from src.endpoints.gst_registration import gst_registration  # noqa: E402
    api.register_blueprint(gst_registration, url_prefix='/gst_registration')

    # Jurisdiction Endpoints
    from src.endpoints.jurisdictions import jurisdictions  # noqa: E402
    api.register_blueprint(jurisdictions, url_prefix='/jurisdictions')

    # LineOfBusinessSectors Endpoints
    from src.endpoints.lob_sectors import lob_sectors  # noqa: E402
    api.register_blueprint(lob_sectors, url_prefix='/lob_sectors')

    # Log Endpoints
    from src.endpoints.logs import logs  # noqa: E402
    api.register_blueprint(logs, url_prefix='/logs')

    # MasterModel Endpoints
    from src.endpoints.master_models import master_models  # noqa: E402
    api.register_blueprint(master_models, url_prefix='/master_models')

    # ParedownRule Endpoints
    from src.endpoints.paredown_rules import paredown_rules  # noqa: E402
    api.register_blueprint(paredown_rules, url_prefix='/paredown_rules')

    # Project Endpoints
    from src.endpoints.projects import projects  # noqa: E402
    api.register_blueprint(projects, url_prefix='/projects')

    # Role Endpoints
    from src.endpoints.roles import roles  # noqa: E402
    api.register_blueprint(roles, url_prefix='/roles')

    # Tax Rate Endpoint
    from src.endpoints.tax_rates import tax_rates  # noqa: E402
    api.register_blueprint(tax_rates, url_prefix='/tax_rates')

    # Transaction Endpoints
    from src.endpoints.transactions import transactions  # noqa: E402
    api.register_blueprint(transactions, url_prefix='/transactions')

    # User Endpoints
    from src.endpoints.users import users  # noqa: E402
    api.register_blueprint(users, url_prefix='/users')


    #===============================================================================
    # Error Handling

    # Bad Request
    @api.errorhandler(400)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 400', 'payload': [], 'message': err.description}
        return jsonify(response), 400
    # Unauthorized
    @api.errorhandler(401)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 401', 'payload': [], 'message': err.description}
        return jsonify(response), 401
    # Forbidden
    @api.errorhandler(403)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 403', 'payload': [], 'message': err.description}
        return jsonify(response), 403
    # Not Found
    @api.errorhandler(404)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 404', 'payload': [], 'message': err.description}
        return jsonify(response), 404
    # Method Not Allowed
    @api.errorhandler(405)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 405', 'payload': [], 'message': err.description}
        return jsonify(response), 405
    # Conflict
    @api.errorhandler(409)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 409', 'payload': [], 'message': err.description}
        return jsonify(response), 409
    # Unprocessable Entity
    @api.errorhandler(422)
    def _handle_endpoint_error(err):
        response = {'status': 'Error 422', 'payload': [], 'message': err.description}
        return jsonify(response), 422
    # Server Error
    @api.errorhandler(500)
    def _handle_server_error(err):
        response = {'status': 'Error 500', 'payload': [], 'message': err.description}
        return jsonify(response), 500
