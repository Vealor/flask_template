
import functools
from flask import jsonify, abort
from flask_jwt_extended import (verify_jwt_in_request, get_current_user)
from src import jwt
from src.models import BlacklistToken, User

#===============================================================================
### Permission Wrapper

def has_permission(roles):
    def decorator(method):
        @functools.wraps(method)
        def f(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()
            if user.is_superuser:
                return method(*args, **kwargs)
            if user.is_system_administrator or user.role.value in roles:
                return method(*args, **kwargs)
            abort(403)
        return f
    return decorator

#===============================================================================
### JWT Helpers
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
