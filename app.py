from dotenv import load_dotenv
from os import environ as env

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    load_dotenv()   # Getting data from local .env for now
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=env.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI=env.get('DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    migrate.init_app(app, db)

    app.debug = True
    app.TEMPLATES_AUTO_RELOAD = True

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
