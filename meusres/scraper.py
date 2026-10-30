
import requests

from bs4 import BeautifulSoup

from meusres.config import MAX_PAGE_TEXT_LENGTH


def fetch_text(url: str) -> str:
    """
    Fetch a webpage and extract readable text.
    """

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15,
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Could not fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary HTML elements
    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header",
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # Limit extracted content
    return text[:MAX_PAGE_TEXT_LENGTH]
