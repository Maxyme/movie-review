from gino.dialects.asyncpg import JSONB

from app import db


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.BigInteger(), primary_key=True)
    url = db.Column(db.String(), nullable=False)
    result_all = db.Column(JSONB())
    result_no_stop_words = db.Column(JSONB())
