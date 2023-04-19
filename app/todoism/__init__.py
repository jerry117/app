from app.todoism.apis.v1 import api_v1
from flask import Flask
import os
from app.setting import config

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('todoism')
    app.config.from_object(config[config_name])
    register_blueprints(app)
    return app



def register_blueprints(app):
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    # app.register_blueprint(api_v1, url_prefix='/v1', subdomain='api')  # enable subdomain support