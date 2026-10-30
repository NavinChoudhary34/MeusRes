
from meusres.scraper import fetch_text


def test_fetch_text():
    url = "https://www.python.org/"

    text = fetch_text(url)

    assert isinstance(text, str)

    print("Extracted text length:", len(text))
    print("Preview:", text[:500])
