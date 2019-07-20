from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


application = Flask(__name__)
application.config['SECRET_KEY'] = 'dev'

bootstrap = Bootstrap(application)

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://typark:Typ8795!@realestateflaskapp.cofwsnpwtydk.us-east-2.rds.amazonaws.com/typark'


# application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reinvest.db'

db = SQLAlchemy(application)

bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from realtoranalysis import routes