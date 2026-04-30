import uuid
from datetime import datetime

from database.models.document import (
    Document
)
from database.repositories.document_repository import (
    DocumentRepository
)

class DocumentService:

    def __init__(self):

        self.repository = (
            DocumentRepository()
        )

    def find_by_hash(
        self,
        file_hash: str
    ):

        return (
            self.repository.find_by_hash(
                file_hash
            )
        )

    def create_document(
        self,
        source_file: str,
        file_hash: str,
        knowledge_base: str,
        knowledge_scope: str,
        owner_type: str,
        document_type: str,
        tenant_id: str | None = None
    ):

        document = Document(
            document_id=str(uuid.uuid4()),
            knowledge_base=knowledge_base,
            knowledge_scope=knowledge_scope,
            owner_type=owner_type,
            tenant_id=tenant_id,
            document_type=document_type,
            source_file=source_file,
            file_hash=file_hash,
            status="UPLOADED",
            created_at=datetime.utcnow()
        )

        return self.repository.save(
                    document
                )
        
    def update_status(
        self,
        document_id: str,
        status: str
    ):

        return (
            self.repository.update_status(
                document_id=document_id,
                status=status
            )
        )
    
    def get_document(
        self,
        document_id: str
    ):

        return (
            self.repository.get(
                document_id
            )
        )

    def delete_document(
        self,
        document_id: str
    ):

        self.repository.delete(
            document_id
        )

    def get(
        self,
        document_id: str
    ):

        return (
            self.repository.get(
                document_id
            )
        )
    
    def list_documents(
    self,
    knowledge_base: str | None = None
    ):
        return (
            self.repository.list_documents(
                knowledge_base
            )
        )