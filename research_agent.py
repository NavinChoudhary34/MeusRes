
import os
import json
import requests
import ollama

from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OLLAMA_API_KEY")
SEARCH_URL = "https://ollama.com/api/web_search"
MODEL = "qwen3.5:0.8b"

# Project directory
BASE_DIR = Path(__file__).resolve().parent


# Search web using Ollama Web Search API
def search_web(query):

    if not API_KEY:
        raise ValueError(
            "OLLAMA_API_KEY is missing. Add it to your .env file."
        )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": query,
        "max_results": 5
    }

    response = requests.post(
        SEARCH_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    return response.json().get("results", [])


# Fetch full web page content
def fetch_text(url):

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        response.raise_for_status()

    except requests.RequestException as e:
        print(f"Could not fetch {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup([
        "script",
        "style",
        "nav",
        "footer",
        "header"
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    # Limit extracted content
    return text[:8000]


def main():

    user_prompt = input("Enter your prompt: ").strip()

    if not user_prompt:
        print("Prompt cannot be empty.")
        return

    try:
        print("\nSearching the web...")

        results = search_web(user_prompt)

        if not results:
            print("No search results found.")
            return

        # Fetch full web page content
        pages = []

        for item in results:

            url = item.get("url")

            if not url:
                continue

            print(f"Fetching: {url}")

            page_text = fetch_text(url)

            pages.append({
                "title": item.get("title", ""),
                "url": url,
                "snippet": item.get("content", ""),
                "page_text": page_text
            })

        if not pages:
            print("Could not retrieve any web pages.")
            return

        # Prepare research prompt
        prompt = f"""
You are a research assistant.

User request:
{user_prompt}

Instructions:
1. Answer using the supplied research data.
2. Do not invent facts.
3. Clearly organize the answer using Markdown.
4. Include source URLs wherever relevant.
5. Mention when information is insufficient.
6. Distinguish verified information from uncertain claims.

Research data:
{json.dumps(pages, ensure_ascii=False)}
"""

        
        # Invoke local Qwen model
        print("\nGenerating research digest...")

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            think=False,
            options={
                "temperature": 0.2,
                "num_predict": 2048
            }
        )

        # Extract generated answer
        digest = (response.message.content or "").strip()

        # Debug information
        print("\n--- LLM DEBUG ---")
        print("Model:", response.model)
        print("Response content length:", len(digest))
        print("Thinking output length:",
            len(response.message.thinking or ""))

        # Stop if the model did not generate an answer
        if not digest:
            print("\nLLM returned empty content.")
            print("Raw response:", response.model_dump_json(indent=2))
            return

        print("\nDigest generated successfully.")


        # Save digest
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = f"digest-{timestamp}.md"
        output_path = BASE_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(digest)

        print(f"\nResearch completed!")
        print(f"Saved to: {output_path}")

    except requests.HTTPError as e:
        print(f"\nWeb search HTTP error: {e}")

        if e.response is not None:
            print("Response:", e.response.text)

    except requests.RequestException as e:
        print(f"\nNetwork error: {e}")

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
