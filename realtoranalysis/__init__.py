from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


application = Flask(__name__)
application.config['SECRET_KEY'] = '#ENTERKEYHERE'

bootstrap = Bootstrap(application)

application.config['SQLALCHEMY_DATABASE_URI'] = '#ENTERCREDENTIALSHERE'

db = SQLAlchemy(application)

bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from realtoranalysis import routes
