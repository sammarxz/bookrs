import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
<<<<<<< HEAD
    SECRET_KEY = os.environ['SECRET_KEY']
=======
    SECRET_KEY = '9bciva5819$gn$a$l*183yau8z3tnwy3-zy6^h$$)!(597y@^d)'
>>>>>>> bc6a26df68ec438d1b0834e2650eb2b6b4e68d8d
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
