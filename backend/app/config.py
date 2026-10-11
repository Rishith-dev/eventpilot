"""Central configuration. Values come from environment variables or the .env file."""
import os
from pathlib import Path

from dotenv import load_dotenv

# backend/app/config.py  ->  parents[2] is the repo root (eventpilot/)
REPO_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(REPO_ROOT / ".env")

DATA_DIR = REPO_ROOT / "data"
RAW_DOCS_DIR = DATA_DIR / "raw"
CHROMA_DIR = DATA_DIR / "chroma"
COLLECTION_NAME = "eventpilot_docs"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
TOP_K = int(os.getenv("TOP_K", "4"))
