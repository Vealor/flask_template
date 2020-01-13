# CUSTOM ERRORS

#===============================================================================

# custom 400 Error
class InputError(Exception):
    pass

# custom 401 Error
class UnauthorizedError(Exception):
    pass

# custom 403 Error
class ForbiddenError(Exception):
    pass

# custom 404 Error
class NotFoundError(Exception):
    pass

# custom 409 Error
class DataConflictError(Exception):
    pass

# custom 422 Error
class UnprocessableEntityError(Exception):
    pass
