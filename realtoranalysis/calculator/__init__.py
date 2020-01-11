from flask import Blueprint


calculator = Blueprint('calculator',
                       __name__,
                       url_prefix='/mortgage_calculator',
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='/static')

from . import views
