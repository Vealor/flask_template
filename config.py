import os
from datetime import timedelta

class Config(object):
    VERSION = '0.1.12'

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # JWT
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=6)
    JWT_ERROR_MESSAGE_KEY = 'message'

class DevelopmentConfig(Config):
    # Statement for enabling the development environment
    DEBUG = True

    # Use a secure, unique and absolutely secret key for signing the data.
    CSRF_SESSION_KEY = "secret"
    # Secret key for signing cookies
    SECRET_KEY = "=!w-tp!0xuqscy*6^er*@l$5s#pu$#*17upk=dg-i_03@##=_)"
    # JWT Secret Key
    JWT_SECRET_KEY = 'jwt-secret-string'

    # Define the database we are working with
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES = {
        'user': 'itra',
        'pw': 'LHDEV1234',
        'db': 'itra_db',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    DATABASE_CONNECT_OPTIONS = {}

class ProductionConfig(Config):
    # Statement for enabling the development environment
    DEBUG = False

    # Use a secure, unique and absolutely secret key for signing the data.
    # CSRF_SESSION_KEY = os.environ['CSRF_SESSION_KEY']
    # Secret key for signing cookies
    # SECRET_KEY = os.environ['SECRET_KEY']
    # JWT Secret Key
    # JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # DATABASE_CONNECT_OPTIONS = {}

del os
