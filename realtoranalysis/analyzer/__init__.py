from flask import Blueprint


analyzer = Blueprint('analyzer',
                     __name__,
                     url_prefix='/analyze',
                     template_folder='templates',
                     static_folder='static',
                     static_url_path='/static')

from . import views
