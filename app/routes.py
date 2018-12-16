import json
import operator
from urllib.parse import urlparse

import requests
from gino import Gino
from quart import Blueprint
from quart import render_template, request

from app import app
from models import Result
from utilities.count_words import spacy_count_entities, text_from_html

simple_app = Blueprint('simple_app', __name__)

app = app
db = Gino(app)


@simple_app.route('/index')
@simple_app.route('/', methods=['GET', 'POST'])
async def index():
    return await render_template('index.html')


@simple_app.route('/start', methods=['POST'])
async def get_counts():
    # get url
    json_data = await request.get_json()
    url = json_data["url"]

    parsed_url = urlparse(url)
    if parsed_url.scheme is "":
        url = 'http://' + url

    return await count_and_save_words(url)


async def count_and_save_words(url):
    try:
        r = requests.get(url)
    except:
        return {"error": "Unable to get URL. Please make sure it's valid and try again."}

    text = text_from_html(r.text)
    raw_word_counter, collected_counter = spacy_count_entities(text)

    # save the results - just for show, much faster to return directly, maybe make a new route?
    result = await Result.create(url=url, result_all=raw_word_counter, result_no_stop_words=collected_counter)

    return_data = dict(sorted(raw_word_counter.items(), key=operator.itemgetter(1), reverse=True)[:10])
    return json.dumps(return_data)
