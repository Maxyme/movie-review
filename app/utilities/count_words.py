import spacy
from bs4 import BeautifulSoup
from bs4.element import Comment
from functools import lru_cache


from stop_words import stops


@lru_cache(maxsize=32)
def spacy_count_entities(text):
    # Load English tokenizer, tagger, parser, NER and word vectors - this can come from
    # import en_core_web_sm; nlp = en_core_web_sm.load()
    nlp = spacy.load('en')  # dynamic loading!
    doc = nlp(text)

    collected_entities = [str(w) for w in doc.ents if str(w) not in stops]
    from collections import Counter
    collected_counter = Counter(collected_entities)

    filtered_entities = [str(entity) for entity in doc.ents if str(entity) not in stops]
    from collections import Counter
    filtered_word_counter = Counter(filtered_entities)

    return filtered_word_counter, collected_counter


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


@lru_cache(maxsize=32)
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


if __name__ == '__main__':
    # debug spacy count
    import requests
    url = "http://nytimes.com"
    r = requests.get(url)
    text = text_from_html(r.text)
    counter = spacy_count_entities(text)
