from flask import Blueprint
from watchlist.setting import config
import os

config_name = os.getenv('FLASK_CONFIG', 'development')

auth = Blueprint('auth', __name__)

@auth.route('/authlogin')
def authlogin():
    print(config[config_name])
    return {'code':200}

@auth.route('/authlogout')
def authlogout():
    return {'code':200}

