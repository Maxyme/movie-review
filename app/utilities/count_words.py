import os
import re

import nltk
from bs4 import BeautifulSoup

from stop_words import stops
NLKT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'nltk_data'))


def count_words(text):
    # text processing
    raw = BeautifulSoup(text).get_text()
    nltk.data.path.append(NLKT_PATH)
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)

    # remove punctuation, count raw words
    non_punct = re.compile('.*[A-Za-z].*')
    raw_words = [w for w in text if non_punct.match(w)]
    raw_word_count = nltk.Counter(raw_words)

    # stop words
    no_stop_words = [w for w in raw_words if w.lower() not in stops]
    no_stop_words_count = nltk.Counter(no_stop_words)

    return raw_word_count, no_stop_words_count
