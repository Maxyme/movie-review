from utilities.count_words import text_from_html, spacy_count_entities


def test_count_words():
    raw_text = "<!DOCTYPE html><html lang=\"en\" xmlns:og=\"http://opengraphprotocol.org/schema/\">test</html>"
    text = text_from_html(raw_text)
    assert text == "test"
