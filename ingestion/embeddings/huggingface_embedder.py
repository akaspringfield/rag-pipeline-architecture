from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import EMBED_MODEL

from ingestion.embeddings.embedding_provider import (
    EmbeddingProvider
)


class HuggingFaceEmbedder(
    EmbeddingProvider
):

    def get_embeddings(self):

        return HuggingFaceEmbeddings(
            model_name=EMBED_MODEL
        )