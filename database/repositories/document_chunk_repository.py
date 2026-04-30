from database.connection import (
    SessionLocal
)

from database.entities.document_chunk_entity import (
    DocumentChunkEntity
)

from database.models.document_chunk import (
    DocumentChunk
)


class DocumentChunkRepository:

    def save(
        self,
        chunk: DocumentChunk
    ):

        db = SessionLocal()

        try:

            entity = DocumentChunkEntity(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                chunk_index=chunk.chunk_index,
                knowledge_base=chunk.knowledge_base,
                knowledge_scope=chunk.knowledge_scope,
                owner_type=chunk.owner_type,
                tenant_id=chunk.tenant_id,
                content=chunk.content,
                source=chunk.source,
                created_at=chunk.created_at
            )

            db.add(entity)

            db.commit()

            return chunk

        finally:

            db.close()

    def save_many(
        self,
        chunks: list
    ):

        db = SessionLocal()

        try:

            entities = []

            for chunk in chunks:

                entities.append(
                    DocumentChunkEntity(
                        chunk_id=chunk.chunk_id,
                        document_id=chunk.document_id,
                        chunk_index=chunk.chunk_index,
                        knowledge_base=chunk.knowledge_base,
                        knowledge_scope=chunk.knowledge_scope,
                        owner_type=chunk.owner_type,
                        tenant_id=chunk.tenant_id,
                        content=chunk.content,
                        source=chunk.source,
                        created_at=chunk.created_at
                    )
                )

            db.add_all(
                entities
            )

            db.commit()

        finally:

            db.close()

    def get_by_document(
        self,
        document_id: str
    ):

        db = SessionLocal()

        try:

            return (
                db.query(
                    DocumentChunkEntity
                )
                .filter(
                    DocumentChunkEntity.document_id
                    == document_id
                )
                .all()
            )

        finally:

            db.close()

    def count_by_document(
        self,
        document_id: str
    ):

        db = SessionLocal()

        try:

            return (
                db.query(
                    DocumentChunkEntity
                )
                .filter(
                    DocumentChunkEntity.document_id
                    == document_id
                )
                .count()
            )

        finally:

            db.close()

    def delete_by_document(
        self,
        document_id: str
    ):

        db = SessionLocal()

        try:

            (
                db.query(
                    DocumentChunkEntity
                )
                .filter(
                    DocumentChunkEntity.document_id
                    == document_id
                )
                .delete()
            )

            db.commit()

        finally:

            db.close()