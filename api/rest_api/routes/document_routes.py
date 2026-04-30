from fastapi import APIRouter

from common.logger import log_error
from services.ingestion_job_service import (
    IngestionJobService
)

router = APIRouter()

@router.get("/jobs/{job_id}")
def get_job(job_id: str):

    try:

        job = (
            IngestionJobService()
            .get(job_id)
        )

        return {
            "job_id": job.job_id,
            "status": job.status,
            "progress": job.progress
        }
    
    except Exception as e:  
        log_error("INGESTION_FAILED", str(e))
        return {
            "error": "Failed to retrieve job status"
        }
        