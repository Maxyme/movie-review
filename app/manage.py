"""manage.py it used to make migrations."""
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

# import models to make the migration
from models import *
Migrate(app, db)
