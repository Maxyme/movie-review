import operator

import requests
from flask import render_template, request

import json

from rq.job import Job

from app import q, app, db
from models import Result

from utilities.count_words import count_words
from worker import conn


@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def get_counts():
    # get url
    data = json.loads(request.data.decode())
    url = data["url"]
    if 'http://' not in url[:7]:
        url = 'http://' + url

    job = q.enqueue_call(func=count_and_save_words, args=(url,), result_ttl=5000)

    return job.get_id()


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(result.result_no_stop_words.items(), key=operator.itemgetter(1), reverse=True)[:10]
        return json.dumps(dict(results))
    else:
        return "Not ready yet!", 202


def count_and_save_words(url):
    try:
        r = requests.get(url)
    except:
        return {"error": "Unable to get URL. Please make sure it's valid and try again."}

    raw_word_count, no_stop_words_count = count_words(r.text)

    # save the results
    result = Result(url=url, result_all=raw_word_count, result_no_stop_words=no_stop_words_count)
    try:
        db.session.add(result)
        db.session.commit()
    except:
        return {"error": "Unable to add item to database."}

    return result.id
