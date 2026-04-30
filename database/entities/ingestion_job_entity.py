from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from database.base import Base


class IngestionJobEntity(Base):

    __tablename__ = "ingestion_jobs"

    job_id = Column(
        String,
        primary_key=True
    )

    document_id = Column(String)

    status = Column(String)

    progress = Column(Integer)

    error_message = Column(
            String,
            nullable=True
        )
    created_at = Column(DateTime)