import concurrent
import json
import operator
from asyncio import get_event_loop
from urllib.parse import urlparse

import aiohttp
from aiocache import cached
from gino import Gino
from quart import Blueprint, websocket
from quart import render_template, request
from quart_cors import cors

from app import app
from models import Result
from utilities.count_words import count_ents

simple_app = Blueprint('simple_app', __name__)
simple_app = cors(simple_app)

app = app
db = Gino(app)


@simple_app.route('/index')
@simple_app.route('/', methods=['GET', 'POST'])
async def index():
    return await render_template('index.html')


@simple_app.route('/getcounts', methods=['POST'])
async def get_counts():
    json_data = await request.get_json()
    url = json_data["url"]

    parsed_url = urlparse(url)
    if parsed_url.scheme is "":
        url = 'http://' + url

    entities = await ents_from_url(url)
    #data = {'a': 4, 'b': 1, 'e': 1}
    entities = [{'name': str(key), 'count': value} for key, value in entities.items()]
    # save the results - just for show, much faster to return directly, maybe make a new route?
    result = await Result.create(url=url, entities=entities)
    return json.dumps(entities)


@cached(ttl=600)
async def ents_from_url(url):
    # todo: it would be great to replace this with asks and pass the quart loop.
    # Update, it works with quart-trio, but not gino, which relies on asyncio...
    # response = await asks.get(url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as s:
                response = await s.read()
        except aiohttp.ClientError as error:
            return {"error": f"Unable to get URL: {error}"}

    html = response.decode()

    # Note, this works for hyperloop with asyncio or uvloop worker but not trio
    loop = get_event_loop()

    # Run cpu heavy work in a thread pool:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        entities = await loop.run_in_executor(pool, count_ents, html)

    return entities


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
