from flask_sqlalchemy import SQLAlchemy
from gino.dialects.asyncpg import JSONB

try:
    from app import db
except ImportError:
    # this is to allow migrations to work when using manage.py
    db = SQLAlchemy()


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.BigInteger(), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    entities = db.Column(JSONB())
