from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Text
from database.base import Base

 
class DocumentChunkEntity(Base):

    __tablename__ = "document_chunks"

    chunk_id = Column(
        String,
        primary_key=True
    )

    document_id = Column(String)

    chunk_index = Column(
        Integer
    )

    knowledge_base = Column(
        String
    )

    knowledge_scope = Column(
        String
    )

    owner_type = Column(
        String
    )

    tenant_id = Column(
        String,
        nullable=True
    )
    
    content = Column(Text)

    source = Column(String)

    created_at = Column(DateTime)