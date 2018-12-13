import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rq import Queue
from worker import conn

app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS', 'config.DevelopmentConfig'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

q = Queue(connection=conn)

from routes import *  # noqa routes need to be imported for flask.
