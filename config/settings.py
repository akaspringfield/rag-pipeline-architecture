from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
CHROMA_DIR = os.getenv("CHROMA_DIR")
EMBED_MODEL = os.getenv("EMBED_MODEL")
TOP_K_FAQ = int(os.getenv("TOP_K_FAQ"))
TOP_K_TICKETS = int(os.getenv("TOP_K_TICKETS"))
TOP_K_GUIDES = os.getenv("TOP_K_GUIDES")
LLM_MODEL = os.getenv("LLM_MODEL")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE"))
MIN_SIMILARITY_SCORE = float(os.getenv("MIN_SIMILARITY_SCORE"))
MIN_RERANK_SCORE = float(os.getenv("MIN_RERANK_SCORE"))
TOP_K = int(os.getenv("TOP_K"))

VECTOR_TOP_K = int(os.getenv("VECTOR_TOP_K"))
BM25_TOP_K = int(os.getenv("BM25_TOP_K"))
RRF_K = int(os.getenv("RRF_K"))
FINAL_CONTEXT_CHUNKS = int(os.getenv("FINAL_CONTEXT_CHUNKS"))

