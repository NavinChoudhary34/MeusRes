
import requests

from meusres.config import (
    OLLAMA_API_KEY,
    SEARCH_URL,
    MAX_SEARCH_RESULTS,
)


def search_web(query: str) -> list:
    """
    Search the web using the Ollama Web Search API.
    """

    if not OLLAMA_API_KEY:
        raise ValueError(
            "OLLAMA_API_KEY is missing. Add it to your .env file."
        )

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "query": query,
        "max_results": MAX_SEARCH_RESULTS,
    }

    response = requests.post(
        SEARCH_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    return response.json().get("results", [])
