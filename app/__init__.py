"""Creating the app"""

import os
from flask import Flask
from flask_jwt_extended import JWTManager

from instance.config import app_config


from app import database_connect
from .api.v2.views.user_views import auth
from .api.v2.views.meetup_views import meetupbp
from .api.v2.views.question_views import questionbp
from .api.v2.views.comment_views import commentbp


def create_app(config_name):
    '''create app using correct configurations'''

    database_connect.create_tables()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv("SECRET")
    jwt = JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(meetupbp)
    app.register_blueprint(questionbp)
    app.register_blueprint(commentbp)

    return app
