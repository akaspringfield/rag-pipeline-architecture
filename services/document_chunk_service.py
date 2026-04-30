import uuid
from datetime import datetime

from database.models.document_chunk import (
    DocumentChunk
)

from database.repositories.document_chunk_repository import (
    DocumentChunkRepository
)


class DocumentChunkService:

    def __init__(self):

        self.repository = (
            DocumentChunkRepository()
        )

    def get_document_chunks(
        self,
        document_id: str
    ):
        return (
            self.repository.get_by_document(
                document_id
            )
        )
    
    def create_chunk(
        self,
        document_id,
        chunk_index
    ):

        chunk = DocumentChunk(
            chunk_id=str(uuid.uuid4()),
            document_id=document_id,
            chunk_index=chunk_index,
            created_at=datetime.utcnow()
        )

        return self.repository.save(
            chunk
        )
    
    def save_chunks(
        self,
        document_id: str,
        chunks: list,
        knowledge_base: str,
        knowledge_scope: str,
        owner_type: str,
        tenant_id: str | None
    ):

        records = []

        for index, chunk in enumerate(chunks):

            records.append(
                DocumentChunk(
                    chunk_id=str(
                        uuid.uuid4()
                    ),
                    document_id=document_id,
                    chunk_index=index,
                    knowledge_base=knowledge_base,
                    knowledge_scope=knowledge_scope,
                    owner_type=owner_type,
                    tenant_id=tenant_id,
                    content=chunk.page_content,
                    source=chunk.metadata.get(
                        "source",
                        ""
                    ),
                    created_at=datetime.utcnow()
                )
            )

        self.repository.save_many(
            records
        )

        return records
    
    def delete_document_chunks(
        self,
        document_id: str
    ):

        self.repository.delete_by_document(
            document_id
        )