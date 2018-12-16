from flask_migrate import Migrate
from gino.ext.quart import Gino
from quart import Quart


app = Quart(__name__)
# Load config
app.config.from_pyfile('settings.py')

# initialize db
db = Gino(app)
Migrate(app, db)

# import and register blueprints
from routes import simple_app
app.register_blueprint(simple_app)
