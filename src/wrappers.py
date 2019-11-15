### WRAPPERS

import functools
from flask import jsonify, abort
from flask_jwt_extended import (verify_jwt_in_request, get_current_user)
from src.errors import *
from src.models import *

#===============================================================================
### Exception Wrapper

def exception_wrapper():
    def decorator(method):
        @functools.wraps(method)
        def f(*args, **kwargs):

            try:
                return method(*args, **kwargs)
            except (InputError, ValueError) as e:
                db.session.rollback()
                abort(400, str(e)) if str(e) else abort(400)
            except (UnauthorizedError) as e:
                db.session.rollback()
                abort(401, str(e)) if str(e) else abort(401)
            except (ForbiddenError) as e:
                db.session.rollback()
                abort(403, str(e)) if str(e) else abort(403)
            except NotFoundError as e:
                db.session.rollback()
                abort(404, str(e)) if str(e) else abort(404)
            except Exception as e:
                db.session.rollback()
                abort(500, str(e)) if str(e) else abort(500)

        return f
    return decorator

#===============================================================================
### Permission Wrapper

def has_permission(roles):
    def decorator(method):
        @functools.wraps(method)
        def f(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()
            if user.is_superuser or user.is_system_administrator or user.role.value in roles:
                return method(*args, **kwargs)
            raise ForbiddenError("You do not have access to this resource.")
        return f
    return decorator
