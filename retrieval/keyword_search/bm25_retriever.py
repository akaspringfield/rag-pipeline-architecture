from langchain_core.documents import Document

from retrieval.keyword_search.bm25_index import (
    BM25Index
)

from database.connection import SessionLocal
from database.entities.document_chunk_entity import (
    DocumentChunkEntity
)


class BM25Retriever:

    def __init__(self):

        self.index = (
            BM25Index.get_instance()
        )


    def load(self):

        if self.index.is_loaded:
            return

        db = SessionLocal()

        try:

            rows = (
                db.query(
                    DocumentChunkEntity
                ).all()
            )

            docs = []

            for row in rows:

                docs.append(

                    Document(
                        page_content=row.content,
                        metadata={
                            "document_id": row.document_id,
                            "chunk_index": row.chunk_index,
                            "source": row.source,
                            "knowledge_base": getattr(row, "knowledge_base", None),
                            "knowledge_scope": getattr(row, "knowledge_scope", None),
                            "owner_type": getattr(row, "owner_type", None),
                            "tenant_id": getattr(row, "tenant_id", None),
                        }
                    )

                )

            self.index.build(docs)

        finally:

            db.close()

    def search(
        self,
        query,
        top_k=20
    ):

        return self.index.search(
            query=query,
            top_k=top_k
        )