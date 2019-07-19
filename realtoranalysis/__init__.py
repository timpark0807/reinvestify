from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

bootstrap = Bootstrap(app)


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://typark:Typ8795!@realestateflaskapp.cofwsnpwtydk.us-east-2.rds.amazonaws.com'


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reinvest.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from realtoranalysis import routes