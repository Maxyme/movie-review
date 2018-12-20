from collections import Counter

import en_core_web_sm
from bs4 import BeautifulSoup
from bs4.element import Comment

# Load English tokenizer, tagger, parser, NER and word vectors - this can come from
# nlp = spacy.load('en')  # dynamic loading!, but linking needs to happen on heroku
# this takes a bit to load, so it's better to have it outside of the function
nlp = en_core_web_sm.load()


def count_ents(text):
    text = text_from_html(text)
    entities = spacy_count_entities(text)
    return entities


def spacy_count_entities(text):
    doc = nlp(text)
    entities = doc.ents
    return Counter([key.string for key in entities])


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
