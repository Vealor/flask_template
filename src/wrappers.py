### WRAPPERS

import functools
from flask import abort
from flask_jwt_extended import (verify_jwt_in_request, get_current_user)
from src.errors import InputError, UnauthorizedError, ForbiddenError, NotFoundError, DataConflictError, UnprocessableEntityError
from src.models import db

#===============================================================================
### Exception Wrapper

def exception_wrapper(method):
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
        except(DataConflictError) as e:
            db.session.rollback()
            abort(409, str(e)) if str(e) else abort(409)
        except(UnprocessableEntityError) as e:
            db.session.rollback()
            abort(422, str(e)) if str(e) else abort(422)
        except Exception as e:
            db.session.rollback()
            abort(500, str(e)) if str(e) else abort(500)

    return f

#===============================================================================
### Permission Wrapper

def has_permission(roles):
    def decorator(method):
        @functools.wraps(method)
        def f(*args, **kwargs):
            verify_jwt_in_request()
            user = get_current_user()
            if user.is_superuser or user.role.value in roles:
                return method(*args, **kwargs)
            raise ForbiddenError("You do not have access to this resource.")
        return f
    return decorator
