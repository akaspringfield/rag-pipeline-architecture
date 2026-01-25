import os

os.environ["TRANSFORMERS_VERBOSITY"] = "error"

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from api.rest_api.routes import router

app = FastAPI(
    title="RAG Platform",
    version="1.0.0"
)

app.include_router(router)