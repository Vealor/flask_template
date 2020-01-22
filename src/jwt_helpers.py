### JWT HELPERS

from flask import jsonify
from src.errors import UnauthorizedError
from src.models import BlacklistToken, User
from src.wrappers import exception_wrapper

#===============================================================================
### JWT Helpers
def build_jwt_helpers(jwt):
    @jwt.user_loader_callback_loader
    @exception_wrapper()
    def user_loader_callback(identity):
        user = User.find_by_username(identity)
        if not user:
            return None
        if not user.is_active:
            raise UnauthorizedError("This account is deactivated")
        return user

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        return jsonify({"message": "User not found"}), 404

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return BlacklistToken.is_blacklisted(jti)
