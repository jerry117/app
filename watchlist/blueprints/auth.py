from flask import Blueprint
from watchlist.setting import config
import os
from watchlist import app

config_name = os.getenv('FLASK_CONFIG', 'development')
# 导入方式
# app.config.from_object(config[config_name])

auth = Blueprint('auth', __name__)

@auth.route('/authlogin')
def authlogin():
    print(config[config_name])
    return {'code':200}

@auth.route('/authlogout')
def authlogout():
    return {'code':200}

