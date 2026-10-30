
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Store the SQLite database inside the data folder
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'meusres.db'}"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# Create database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Base class for all database models
class Base(DeclarativeBase):
    pass
