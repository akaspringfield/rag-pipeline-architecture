from langchain_chroma import Chroma

from config.settings import (
    CHROMA_DIR
)

from ingestion.indexing.vector_store_provider import (
    VectorStoreProvider
)


class ChromaIndexer(
    VectorStoreProvider
):

    def __init__(
        self,
        collection_name: str,
        embeddings
    ):

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR
        )

    def add_documents(
        self,
        documents: list
    ):

        self.vector_store.add_documents(
            documents
        )

    def delete_document(
        self,
        document_id: str
    ):

        self.vector_store._collection.delete(
            where={
                "document_id": document_id
            }
        )