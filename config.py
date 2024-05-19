import os

class Config(object):
    # Get the absolute path of the directory containing the current Python script
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'itsasecret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Set the upload folder path by joining BASE_DIR with a subdirectory named 'uploads'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

class TestConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
    TESTING = True
    TF_CSRF_ENABLED = False  # Disable CSRF protection in tests
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')#
