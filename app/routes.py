import json
import operator
from asyncio import get_event_loop
from urllib.parse import urlparse

import aiohttp
from aiocache import cached
from gino import Gino
from quart import Blueprint, websocket
from quart import render_template, request

from app import app
from models import Result
from utilities.count_words import count_ents

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

    raw_word_counter, collected_counter = await ents_from_url(url)

    # save the results - just for show, much faster to return directly, maybe make a new route?
    result = await Result.create(url=url, result_all=raw_word_counter, result_no_stop_words=collected_counter)

    return_data = dict(sorted(raw_word_counter.items(), key=operator.itemgetter(1), reverse=True)[:10])
    return json.dumps(return_data)


@cached(ttl=600)
async def ents_from_url(url):
    # todo: it would be great to replace this with asks and pass the quart loop
    # response = await asks.get(url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as s:
                response = await s.read()
        except aiohttp.ClientError as error:
            return {"error": f"Unable to get URL: {error}"}

    html = response.decode()

    # todo: can this be the quart event loop? what happens with trio or uvloop??
    loop = get_event_loop()
    print(loop)
    raw_word_counter, collected_counter = await loop.run_in_executor(None, count_ents, html)

    return raw_word_counter, collected_counter


@app.websocket('/ws')
async def ws():
    while True:
        data = await websocket.receive()
        data = json.loads(data)
        url = data["url"]
        parsed_url = urlparse(url)
        if parsed_url.scheme is "":
            url = 'http://' + url

        await websocket.send(f"echo {url}")
