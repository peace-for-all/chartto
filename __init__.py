#from flask import Flask
#from flask_session import Session
#from logic import Analyzer
#from core.validator import Validator
#from core.user import User
#from utils import date2d3
from dotenv import load_dotenv
from os import environ as env

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Local imports
# import models

APP_NAME = 'chartto'    # wx3: mv to sep conf class later

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()   # Getting data from local .env for now
    app = Flask(APP_NAME)
    app.config.from_mapping(
        SECRET_KEY = env.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate.init_app(app, db)

    app.debug = True
    app.TEMPLATES_AUTO_RELOAD = True

    # from . import models

    return app

# APP_NAME = 'todoist-charts'
# app = Flask(APP_NAME)
# SESSION_TYPE = 'memcached'
# app.config.from_object(__name__)
# Session(app)
# v = Validator()


if __name__ == '__main__':
    app = create_app()
    app.run()
