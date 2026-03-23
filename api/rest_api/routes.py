from fastapi import APIRouter, Depends

from api.rest_api.schemas import KnowledgeRequest
from api.rest_api.dependencies import get_knowledge_service
from common.exceptions import KnowledgeBaseEmptyException

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

    except KnowledgeBaseEmptyException:

        return {
            "user_id": user_id,
            "answer": None,
            "message": "No data available in knowledge base"
        }