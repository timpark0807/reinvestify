from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_redis import FlaskRedis

application = Flask(__name__)
redis_client = FlaskRedis(application)

application.config['SECRET_KEY'] = '#ENTERKEYHERE'
bootstrap = Bootstrap(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reinvest.db'

# REDIS_URL = "redis://localhost:6379/0"
#
db = SQLAlchemy(application)

bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from .calculator import calculator
from .analyzer import analyzer

application.register_blueprint(calculator)
application.register_blueprint(analyzer)

from realtoranalysis import routes
