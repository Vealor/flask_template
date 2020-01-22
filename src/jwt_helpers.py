### JWT HELPERS

from flask import jsonify
from src.core.models import BlacklistToken, User

#===============================================================================
### JWT Helpers
def build_jwt_helpers(jwt):
    @jwt.user_loader_callback_loader
    def user_loader_callback(identity):
        user = User.find_by_username(identity)
        if not user:
            return None
        return user

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        return jsonify({"message": "User not found"}), 404

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return BlacklistToken.is_blacklisted(jti)
