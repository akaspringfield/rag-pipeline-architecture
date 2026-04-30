from uuid import uuid4
from datetime import datetime

from database.models.ingestion_job import (
    IngestionJob
)

from database.repositories.ingestion_job_repository import (
    IngestionJobRepository
)


class IngestionJobService:

    def __init__(self):

        self.repository = (
            IngestionJobRepository()
        )

    def create_job(
        self,
        document_id
    ):

        job = IngestionJob(
            job_id=str(uuid4()),
            document_id=document_id,
            status="UPLOADED",
            progress=0,
            error_message=None,
            created_at=datetime.utcnow()
        )

        return self.repository.save(
            job
        )


    def update_status(
        self,
        job_id,
        status,
        progress
    ):

        print(
            f"[JOB_UPDATE] {job_id}"
            f" => {status}"
            f" ({progress}%)"
        )

        return self.repository.update_status(
            job_id,
            status,
            progress
        )
    
    def update(
        self,
        job_id,
        status,
        progress
    ):

        return self.repository.update_status(
            job_id,
            status,
            progress
        )

    def mark_failed(
        self,
        job_id,
        error_message
    ):
        self.update_status(
            job_id,
            "FAILED",
            0
        )