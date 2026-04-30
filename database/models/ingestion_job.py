from dataclasses import dataclass
from datetime import datetime


@dataclass
class IngestionJob:

    job_id: str

    document_id: str

    status: str

    progress: int

    error_message: str | None = None

    created_at: datetime = datetime.utcnow()
    