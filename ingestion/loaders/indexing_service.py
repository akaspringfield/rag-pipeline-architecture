from langchain_chroma import Chroma

from ingestion.embeddings.embedding_service import (
    EmbeddingService
)

from config.settings import (
    CHROMA_DIR
)


class IndexingService:

    def __init__(self):

        self.embeddings = (
            EmbeddingService()
            .get_embeddings()
        )

    def index(
        self,
        docs,
        collection_name: str
    ):

        vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_DIR
        )

        vectorstore.add_documents(
            docs
        )

        return len(docs)