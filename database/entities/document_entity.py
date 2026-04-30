from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime

from database.base import Base


class DocumentEntity(Base):

    __tablename__ = "documents"

    document_id = Column(
        String,
        primary_key=True
    )

    knowledge_base = Column(String)

    knowledge_scope = Column(String)

    owner_type = Column(String)

    tenant_id = Column(String,nullable=True)

    document_type = Column(String)

    source_file = Column(String)

    file_hash = Column(
        String,
        unique=True
    )

    status = Column(String)

    created_at = Column(DateTime)