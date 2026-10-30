
# MeusRes – AI-Powered Personal Research Assistant

**MeusRes** is an AI-powered personal research assistant that automates the process of searching, collecting, analyzing, and summarizing information from the web.

Instead of manually visiting multiple websites and organizing information, users can enter a research query and receive an AI-generated research digest backed by collected web sources.

The application combines web search, web scraping, a locally running Large Language Model (LLM), and persistent storage to create a simple end-to-end research workflow.

> **Project Status:** v0.1 – Working Prototype

---

## Key Features

- **AI-Powered Research:** Enter a topic or question and generate a research digest.
- **Web Search Integration:** Retrieve relevant web results using the Ollama Web Search API.
- **Web Content Extraction:** Extract readable text from relevant web pages using BeautifulSoup.
- **Local LLM Processing:** Generate research summaries using a locally running Ollama model.
- **Research Persistence:** Store research queries, generated answers, and source information in an SQLite database.
- **REST API:** Expose research functionality through a FastAPI backend.
- **Interactive Dashboard:** Use a Streamlit interface to initiate research and explore previous results.
- **Research History:** Access previously completed research runs.
- **Markdown Export:** Download generated research digests for future reference.

---

## How It Works

MeusRes follows a sequential research pipeline:

```text
             User Research Query
                     |
                     v
              Streamlit Frontend
                     |
                     v
                FastAPI Backend
                     |
                     v
                Research Pipeline
                     |
                     v
             Ollama Web Search API
                     |
                     v
              Relevant Web Results
                     |
                     v
               Web Scraping
                     |
                     v
             Content Extraction
                     |
                     v
              Local Ollama LLM
                     |
                     v
             AI Research Digest
                     |
                     v
              SQLite Database
                     |
                     v
              Display Results
```

### Research Workflow

1. **Query Submission:** The user enters a research topic through the Streamlit interface.
2. **Web Search:** The backend sends the query to the Ollama Web Search API to retrieve relevant results.
3. **Content Extraction:** BeautifulSoup extracts readable text from the retrieved web pages.
4. **AI Processing:** The extracted information and source details are passed to the locally running Ollama model.
5. **Digest Generation:** The LLM generates a structured research digest.
6. **Data Persistence:** The research query, generated response, and source information are saved in SQLite.
7. **Result Presentation:** The frontend displays the generated digest and collected sources.

---

## Technology Stack

| Component              | Technology              |
| ---------------------- | ----------------------- |
| Programming Language   | Python 3.12             |
| Package Management     | uv                      |
| LLM Runtime            | Ollama                  |
| LLM Model              | Qwen 3.5 0.8B           |
| Web Search             | Ollama Web Search API   |
| Web Scraping           | Requests, BeautifulSoup |
| Backend                | FastAPI                 |
| Frontend               | Streamlit               |
| Database               | SQLite                  |
| ORM                    | SQLAlchemy              |
| API Validation         | Pydantic                |
| Environment Management | python-dotenv           |
| Testing                | pytest                  |

---

## Project Structure

```text
MeusRes/
│
├── meusres/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── init_db.py
│   ├── search.py
│   ├── scraper.py
│   ├── llm.py
│  
```
