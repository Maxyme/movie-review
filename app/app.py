"""main entry point for the app"""

from gino.ext.quart import Gino
from quart import Quart
from quart_cors import cors

app = Quart(__name__)

# load config
app.config.from_pyfile('settings.py')

# setting this for now, because current quart-cors extension has an issue with * (default value!)
app = cors(app, allow_headers=['content-type'])

# set the database handler
db = Gino(app)

# import and register blueprints
from routes import simple_app  # noqa, prevent circular imports
app.register_blueprint(simple_app)
