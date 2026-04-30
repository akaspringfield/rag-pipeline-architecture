from fastapi import APIRouter, Depends

from api.rest_api.schemas import KnowledgeRequest
from api.rest_api.dependencies import get_knowledge_service
from common.exceptions import KnowledgeBaseEmptyException

from common.logger import log_error
from common.logger import log_error
from query_processing.query_service import QueryService
from orchestration.solution_orchestrator import SolutionOrchestrator


router = APIRouter()


@router.get("/")
def health():

    return {
        "status": "application running and healthy"
    }



@router.post("/solution/knowledge/{user_id}")
async def knowledge_solution(
    user_id: str,
    request: KnowledgeRequest,
    service=Depends(get_knowledge_service)
):

    try:
        query_service = QueryService()

        context = query_service.process(
            user_id=user_id,
            query=request.query
        )

        orchestrator = SolutionOrchestrator()

        response = orchestrator.execute(
            context
        )

        return {
            "user_id": user_id,
            "query_type": str(context.query_type),
            "answer": response.answer,
            "sources": response.sources
        }

    except KnowledgeBaseEmptyException as e:
        log_error("Knowledge_Base_Empty_Exception_FAILED", str(e))

        return {
            "user_id": user_id,
            "answer": None,
            "message": "No data available in knowledge base"
        }
    
from fastapi import APIRouter

from services.ingestion_job_service import (
    IngestionJobService
)
from services.document_deletion_service import DocumentDeletionService

router = APIRouter()

@router.get("/jobs/{job_id}")
def get_job(job_id: str):

    job = (
        IngestionJobService()
        .get(job_id)
    )

    return {
        "job_id": job.job_id,
        "status": job.status,
        "progress": job.progress
    }


@router.delete(
    "/documents/{document_id}"
)
def delete_document(
    document_id: str
):
    DocumentDeletionService()