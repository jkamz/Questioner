"""Creating the app"""

import os
from flask import Flask
from instance.config import app_config
from .api.v1.views.meetup_views import meetupbp
from .api.v1.views.questions_views import questionbp
from .api.v1.views.user_views import userbp


def create_app(config_name):
    '''create app using correct configurations'''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv("SECRET")

    app.register_blueprint(meetupbp)
    app.register_blueprint(questionbp)
    app.register_blueprint(userbp)

    return app
