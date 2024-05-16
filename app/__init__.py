from flask import Flask
from config import Config, TestConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

if app.config['TESTING']:
    app.config.from_object(TestConfig)
else:
    app.config.from_object(Config)
    
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from app import routes, models

# This is used to load a user from the user_id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
