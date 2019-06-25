
VERSION = '0.1.0'

import os
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Statement for enabling the development environment
DEBUG = False

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sqlite3.db')
DATABASE_CONNECT_OPTIONS = {}
# API DB Config
# POSTGRES = {
#     'user': 'api',
#     'pw': 'KpmgLighthouse1234',
#     'db': 'api_db',
#     'host': 'localhost',
#     'port': '5432',
# }


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "=!w-tp!0xuqscy*6^er*@l$5s#pu$#*17upk=dg-i_03@##=_)"


# JWT
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = 'jwt-secret-string'
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=6)
JWT_ERROR_MESSAGE_KEY = 'message'



del os
