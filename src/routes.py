from flask import jsonify

#===============================================================================
### Endpoint Imports
def build_blueprints(api):

    # ==========================================================================
    # CORE

    # General Endpoints
    from src.core.endpoints.general import general  # noqa: E402
    api.register_blueprint(general, url_prefix='/')

    # Auth Endpoints
    from src.core.endpoints.auth import auth  # noqa: E402
    api.register_blueprint(auth, url_prefix='/auth')

    # CDMLabel Endpoints
    from src.core.endpoints.cdm_labels import cdm_labels  # noqa: E402
    api.register_blueprint(cdm_labels, url_prefix='/core/cdm_labels')

    # Client Endpoints
    from src.core.endpoints.clients import clients  # noqa: E402
    api.register_blueprint(clients, url_prefix='/core/clients')

    # DataMapping Endpoints
    from src.core.endpoints.data_mappings import data_mappings  # noqa: E402
    api.register_blueprint(data_mappings, url_prefix='/core/data_mappings')

    # DataParam Endpoints
    from src.core.endpoints.data_params import data_params  # noqa: E402
    api.register_blueprint(data_params, url_prefix='/core/data_params')

    # Jurisdiction Endpoints
    from src.core.endpoints.jurisdictions import jurisdictions  # noqa: E402
    api.register_blueprint(jurisdictions, url_prefix='/core/jurisdictions')

    # LineOfBusinessSectors Endpoints
    from src.core.endpoints.lob_sectors import lob_sectors  # noqa: E402
    api.register_blueprint(lob_sectors, url_prefix='/core/lob_sectors')

    # Log Endpoints
    from src.core.endpoints.logs import logs  # noqa: E402
    api.register_blueprint(logs, url_prefix='/core/logs')

    # Project Endpoints
    from src.core.endpoints.projects import projects  # noqa: E402
    api.register_blueprint(projects, url_prefix='/core/projects')

    # Role Endpoints
    from src.core.endpoints.roles import roles  # noqa: E402
    api.register_blueprint(roles, url_prefix='/core/roles')

    # User Endpoints
    from src.core.endpoints.users import users  # noqa: E402
    api.register_blueprint(users, url_prefix='/core/users')

    # ==========================================================================
    # ITRA

    # CapsGen Endpoints
    from src.itra.endpoints.caps_gen import caps_gen  # noqa: E402
    api.register_blueprint(caps_gen, url_prefix='/itra/caps_gen')

    # ClientModel Endpoints
    from src.itra.endpoints.client_models import client_models  # noqa: E402
    api.register_blueprint(client_models, url_prefix='/itra/client_models')

    # Client Vendor Master Endpoint
    from src.itra.endpoints.client_vendor_master import client_vendor_master  # noqa: E402
    api.register_blueprint(client_vendor_master, url_prefix='/itra/client_vendor_master')

    # Client Tax GL Extract Endpoint
    from src.itra.endpoints.client_tax_gl_extract import client_tax_gl_extract  # noqa: E402
    api.register_blueprint(client_tax_gl_extract, url_prefix='/itra/client_tax_gl_extract')

    # Code Endpoint
    from src.itra.endpoints.codes import codes  # noqa: E402
    api.register_blueprint(codes, url_prefix='/itra/codes')

    # ErrorCategory Endpoints
    from src.itra.endpoints.error_categories import error_categories  # noqa: E402
    api.register_blueprint(error_categories, url_prefix='/itra/error_categories')

    # FXrates Endpoints
    from src.itra.endpoints.fx_rates import fx_rates  # noqa: E402
    api.register_blueprint(fx_rates, url_prefix='/itra/fx_rates')

    # Gst Registration Endpoint
    from src.itra.endpoints.gst_registration import gst_registration  # noqa: E402
    api.register_blueprint(gst_registration, url_prefix='/itra/gst_registration')

    # MasterModel Endpoints
    from src.itra.endpoints.master_models import master_models  # noqa: E402
    api.register_blueprint(master_models, url_prefix='/itra/master_models')

    # ParedownRule Endpoints
    from src.itra.endpoints.paredown_rules import paredown_rules  # noqa: E402
    api.register_blueprint(paredown_rules, url_prefix='/itra/paredown_rules')

    # Tax Rate Endpoint
    from src.itra.endpoints.tax_rates import tax_rates  # noqa: E402
    api.register_blueprint(tax_rates, url_prefix='/itra/tax_rates')

    # Transaction Endpoints
    from src.itra.endpoints.transactions import transactions  # noqa: E402
    api.register_blueprint(transactions, url_prefix='/itra/transactions')

    # ==========================================================================
    # ROYALTIES

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
