from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from quart import Quart

db = SQLAlchemy()


def create_app(**config_overrides):
    app = Quart(__name__)
    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides (if applicable)
    app.config.update(config_overrides)

    # initialize db
    db.init_app(app)
    Migrate(app, db)

    # import and register blueprints
    from routes import simple_app
    app.register_blueprint(simple_app)

    return app
