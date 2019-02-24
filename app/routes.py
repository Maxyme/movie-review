import concurrent
import json
import os
from asyncio import get_event_loop
from urllib.parse import urlparse

from aiohttp_requests import requests

from aiocache import cached
from gino import Gino
from quart import Blueprint, websocket, redirect
from quart import request
from quart_cors import cors

from app import app
from models import Result
from utilities.count_words import count_ents

simple_app = Blueprint('simple_app', __name__)
simple_app = cors(simple_app)

app = app
db = Gino(app)


@simple_app.route('/index')
@simple_app.route('/', methods=['GET'])
async def index():
    frontend = os.getenv('FRONTEND_URL')
    return redirect(frontend)


@simple_app.route('/getcounts', methods=['POST'])
async def get_counts():
    json_data = await request.get_json()
    url = json_data["url"]

    parsed_url = urlparse(url)
    if parsed_url.scheme is "":
        url = 'http://' + url

    entities = await ents_from_url(url)

    top_10_entities = entities.most_common(10)
    top_10_entities = [{'name': str(key), 'count': value} for key, value in top_10_entities]
    # save the results - just for show, much faster to return directly, maybe make a new route?
    result = await Result.create(url=url, entities=top_10_entities)

    return json.dumps(top_10_entities)


@cached(ttl=600)
async def ents_from_url(url):
    response = await requests.get(url)
    html = response.decode("utf-8", 'ignore')

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
