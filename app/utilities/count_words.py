from collections import Counter

import en_core_web_sm
from bs4 import BeautifulSoup
from bs4.element import Comment

from stop_words import stops


def count_ents(text):
    text = text_from_html(text)
    raw_word_counter, collected_counter = spacy_count_entities(text)
    return raw_word_counter, collected_counter


def spacy_count_entities(text):
    # Load English tokenizer, tagger, parser, NER and word vectors - this can come from
    # nlp = spacy.load('en')  # dynamic loading!, but linking needs to happen on heroku
    nlp = en_core_web_sm.load()
    doc = nlp(text)

    collected_entities = [str(w) for w in doc.ents if str(w) not in stops]
    filtered_entities = [str(entity) for entity in doc.ents if str(entity) not in stops]

    return Counter(filtered_entities), Counter(collected_entities)


def tag_visible(element):
    if isinstance(element, Comment) \
            or element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False

    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


if __name__ == '__main__':
    # debug
    import requests

    url = "http://nytimes.com"
    r = requests.get(url)
    text = text_from_html(r.text)
    counter = spacy_count_entities(text)
