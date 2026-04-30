from ingestion.indexing.vector_store_provider import (
    VectorStoreProvider
)


class QdrantIndexer(
    VectorStoreProvider
):

    def __init__(
        self,
        collection_name: str,
        embeddings
    ):
        pass

    def add_documents(
        self,
        documents: list
    ):
        pass