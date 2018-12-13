import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from rq import Queue

from worker import conn

db = SQLAlchemy()
q = Queue(connection=conn)


def create_app(**config_overrides):
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')
    #app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))

    # apply overrides for tests
    app.config.update(config_overrides)

    # initialize db
    db.init_app(app)
    # db.create_all()  ## ?

    migrate = Migrate(app, db)

    # import and register blueprints
    from routes import simple_app
    app.register_blueprint(simple_app)

    return app
