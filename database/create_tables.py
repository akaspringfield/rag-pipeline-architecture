from database.base import Base
from database.connection import engine

# Import ALL entities
from database.entities.document_entity import DocumentEntity
from database.entities.ingestion_job_entity import IngestionJobEntity
from database.entities.document_chunk_entity import DocumentChunkEntity

print(Base.metadata.tables.keys())

# Base.metadata.create_all(bind=engine)

print("Tables created")