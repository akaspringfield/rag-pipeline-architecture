from database.connection import (
    SessionLocal
)

from database.entities.document_entity import (
    DocumentEntity
)

from database.models.document import (
    Document
)


class DocumentRepository:

    def save(
        self,
        document: Document
    ):

        db = SessionLocal()

        try:

            entity = DocumentEntity(
                document_id=document.document_id,
                knowledge_base=document.knowledge_base,
                knowledge_scope=document.knowledge_scope,
                owner_type=document.owner_type,
                tenant_id=document.tenant_id,
                document_type=document.document_type,
                source_file=document.source_file,
                file_hash=document.file_hash,
                status=document.status,
                created_at=document.created_at
            )

            db.add(entity)

            db.commit()

            print(
                f"[DOCUMENT_SAVED] => "
                f"{document.document_id}"
            )

            return document

        finally:

            db.close()

    def find_by_hash(
        self,
        file_hash: str
    ):

        db = SessionLocal()

        try:

            return (
                db.query(DocumentEntity)
                .filter(
                    DocumentEntity.file_hash
                    == file_hash
                )
                .first()
            )

        finally:

            db.close()

    def get(
        self,
        document_id: str
    ):

        db = SessionLocal()

        try:

            return (
                db.query(DocumentEntity)
                .filter(
                    DocumentEntity.document_id
                    == document_id
                )
                .first()
            )

        finally:

            db.close()

    def delete(
        self,
        document_id: str
    ):

        db = SessionLocal()

        try:

            entity = (
                db.query(DocumentEntity)
                .filter(
                    DocumentEntity.document_id
                    == document_id
                )
                .first()
            )

            if entity:

                db.delete(entity)

                db.commit()

        finally:

            db.close()

    def update_status(
        self,
        document_id: str,
        status: str
    ):

        db = SessionLocal()

        try:

            entity = (
                db.query(DocumentEntity)
                .filter(
                    DocumentEntity.document_id
                    == document_id
                )
                .first()
            )

            if entity:

                entity.status = status

                db.commit()

            return entity

        finally:

            db.close()

    def exists_by_hash(
        self,
        file_hash: str
    ):

        return (
            self.find_by_hash(file_hash)
            is not None
        )
        
    def list_documents(
        self,
        knowledge_base: str | None = None
    ):
        db = SessionLocal()

        try:

            query = db.query(
                DocumentEntity
            )

            if knowledge_base:

                query = query.filter(
                    DocumentEntity.knowledge_base
                    == knowledge_base
                )

            return query.all()

        finally:

            db.close()