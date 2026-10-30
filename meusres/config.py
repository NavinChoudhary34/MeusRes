
import os
from pathlib import Path

from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the project root
load_dotenv(BASE_DIR / ".env")

# Ollama Web Search configuration
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
SEARCH_URL = "https://ollama.com/api/web_search"

# Local Ollama model
MODEL = "qwen3.5:0.8b"

# Research configuration
MAX_SEARCH_RESULTS = 5
MAX_PAGE_TEXT_LENGTH = 8000
