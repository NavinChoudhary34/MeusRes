
import json

from meusres.config import MODEL
from meusres.search import search_web
from meusres.scraper import fetch_text
from meusres.llm import generate_digest
from meusres.research import save_research


def run_research(user_query: str) -> dict:
    """
    Run the complete research workflow:
    search -> scrape -> generate -> save.
    """

    user_query = user_query.strip()

    if not user_query:
        raise ValueError("Research query cannot be empty.")

    # 1. Search the web
    print("\nSearching the web...")

    results = search_web(user_query)

    if not results:
        raise ValueError("No search results found.")

    # 2. Fetch webpage content
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
            "page_text": page_text,
        })

    if not pages:
        raise ValueError("Could not retrieve any web pages.")

    # 3. Build the research prompt
    prompt = f"""
You are a research assistant.

User request:
{user_query}

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

    # 4. Generate the research digest
    digest = generate_digest(prompt)

    # 5. Save research and sources in SQLite
    research_id = save_research(
        query=user_query,
        answer=digest,
        model=MODEL,
        sources=pages,
    )

    print("\nResearch saved successfully.")
    print("Research ID:", research_id)

    # 6. Return the result
    return {
        "research_id": research_id,
        "query": user_query,
        "answer": digest,
        "model": MODEL,
        "sources": pages,
    }
