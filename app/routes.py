import json
import operator

import requests
from quart import Blueprint
from flask_sqlalchemy import SQLAlchemy
from quart import render_template, request

from app import db, create_app
from models import Result
from utilities.count_words import count_words

simple_app = Blueprint('simple_app', __name__)
app = create_app()


@simple_app.route('/index')
@simple_app.route('/', methods=['GET', 'POST'])
async def index():
    return await render_template('index.html')


@simple_app.route('/start', methods=['POST'])
async def get_counts():
    # get url
    data = (await request.data)
    data = json.loads(data.decode())
    url = data["url"]
    if 'http://' not in url[:7]:
        url = 'http://' + url

    return await count_and_save_words(url)


async def count_and_save_words(url):
    try:
        r = requests.get(url)
    except:
        return {"error": "Unable to get URL. Please make sure it's valid and try again."}

    raw_word_count, no_stop_words_count = count_words(r.text)

    # save the results - just for show, much faster to return directly, maybe make a new route?
    result = Result(url=url, result_all=raw_word_count, result_no_stop_words=no_stop_words_count)
    async with app.app_context():
        db = SQLAlchemy(app)
        try:
            db.session.add(result)
            db.session.commit()
        except:
            return {"error": "Unable to add item to database."}, 403

    return json.dumps(dict(sorted(no_stop_words_count.items(), key=operator.itemgetter(1), reverse=True)[:10]))
