"""Creating the app"""

import os
from flask import Flask
from instance.config import app_config

from database_connect import create_tables
from .api.v2.views.user_views import auth


def create_app(config_name):
    '''create app using correct configurations'''

    create_tables()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv("SECRET")

    app.register_blueprint(auth)

    return app
