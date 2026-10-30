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
│   ├── research.py
│   ├── pipeline.py
│   ├── schemas.py
│   └── api.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   ├── test_search.py
│   ├── test_scraper.py
│   ├── test_llm.py
│   ├── test_research.py
│   └── test_pipeline.py
│
├── data/
│   └── exports/
│
├── main.py
├── research_agent.py
├── run_research.py
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── .env.example
└── README.md
```

---

## Getting Started

Follow these instructions to run MeusRes locally.

### 1. Prerequisites

Make sure you have installed:

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/)
- Git

### 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/MeusRes.git
```

Navigate into the project directory:

```bash
cd MeusRes
```

### 3. Install Dependencies

Use uv to install the project dependencies:

```bash
uv sync
```

### 4. Configure the Environment

Create a `.env` file in the project root.

Add your Ollama API key:

```env
OLLAMA_API_KEY=your_ollama_api_key
```

The API key is used for the Ollama Web Search API.

**Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Download the Local LLM

Pull the model using Ollama:

```bash
ollama pull qwen3.5:0.8b
```

Make sure Ollama is running before starting the application.

### 6. Initialize the Database

Run:

```bash
uv run python -m meusres.init_db
```

This initializes the SQLite database and creates the required tables.

---

## Running the Application

MeusRes consists of two main components: a FastAPI backend and a Streamlit frontend.

### Start the Backend

Open a terminal in the project directory:

```bash
uv run uvicorn meusres.api:app --reload
```

The backend will be available at:

`http://127.0.0.1:8000`

FastAPI interactive API documentation:

`http://127.0.0.1:8000/docs`

### Start the Frontend

Open a second terminal:

```bash
uv run streamlit run frontend/app.py
```

The Streamlit application will be available at:

`http://localhost:8501`

Keep both terminals running while using the application.

---

## API Endpoints

The FastAPI backend exposes the following endpoints:

| Method | Endpoint                    | Description                         |
| ------ | --------------------------- | ----------------------------------- |
| GET    | `/`                       | Check backend availability          |
| POST   | `/research`               | Start a new research task           |
| GET    | `/research`               | Retrieve research history           |
| GET    | `/research/{research_id}` | Retrieve a specific research result |

Interactive API documentation is available through FastAPI Swagger UI at `/docs`.

---

## Database

MeusRes uses SQLite with SQLAlchemy for persistent storage.

The database stores two primary entities:

### ResearchRun

Stores information about each research execution:

- Research ID
- User query
- Generated research digest
- LLM model
- Execution status
- Creation timestamp

### Source

Stores information about the sources associated with each research run:

- Source ID
- Associated research ID
- Page title
- Source URL
- Search snippet
- Extracted page content

This allows users to revisit previously completed research without having to execute the same query again.

---

## Testing

The project includes tests for its core components.

Run the test suite using:

```bash
uv run pytest
```

Individual modules can also be tested separately:

```bash
uv run pytest tests/test_search.py
uv run pytest tests/test_scraper.py
uv run pytest tests/test_llm.py
uv run pytest tests/test_research.py
uv run pytest tests/test_pipeline.py
```

---

## Current Limitations

MeusRes is currently a working prototype. Some areas can be improved in future versions:

- Search quality and source relevance can be improved.
- Web scraping currently relies on extracting readable page text and may not work with every website.
- Research output quality depends on the retrieved content and the capabilities of the selected LLM.
- The research pipeline currently executes synchronously.
- Source verification and citation quality can be improved.
- Advanced research planning and multi-step autonomous research are not yet implemented.

---

## Future Improvements

Potential directions for future development include:

- Multi-step agentic research and query decomposition.
- Improved source ranking and relevance evaluation.
- Better source attribution and citation generation.
- Support for multiple LLM providers and models.
- Background task execution for longer research requests.
- Research comparison and follow-up questions.
- More advanced research history and organization.
- Export options such as PDF and DOCX.
- Improved error handling, logging, and monitoring.

---



## License

This project is intended for educational and personal portfolio purposes. A formal open-source license can be added as the project evolves.
