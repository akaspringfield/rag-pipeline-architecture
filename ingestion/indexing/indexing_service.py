from ingestion.indexing.chroma_indexer import (
    ChromaIndexer
)

from ingestion.embeddings.embedding_service import (
    EmbeddingService
)


class IndexingService:

    def __init__(
        self,
        collection_name: str
    ):

        embeddings = (
            EmbeddingService()
            .get_embeddings()
        )

        self.indexer = ChromaIndexer(
            collection_name=collection_name,
            embeddings=embeddings
        )

    def index(
        self,
        documents: list
    ):

        self.indexer.add_documents(
            documents
        )

    def delete_document(
        self,
        document_id: str
    ):

        self.indexer.delete_document(
            document_id
        )