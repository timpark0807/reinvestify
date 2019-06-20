from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

bootstrap = Bootstrap(app)

from realtoranalysis import routes