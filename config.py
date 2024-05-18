import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'itsasecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    TESTING = True
    TESTING = True
    TF_CSRF_ENABLED = False  # Disable CSRF protection in tests