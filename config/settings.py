CHROMA_DIR = "chroma_store"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K_FAQ = 3
TOP_K_TICKETS = 3
TOP_K_GUIDES = 3

LLM_MODEL = "qwen/qwen3-32b"

LLM_TEMPERATURE = 0
MIN_SIMILARITY_SCORE = 1.0

MIN_RERANK_SCORE = 0.30


from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")