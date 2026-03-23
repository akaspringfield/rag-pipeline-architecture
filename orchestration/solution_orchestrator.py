from services.knowledge_service import KnowledgeService
from common.logger import log_step


class SolutionOrchestrator:

    def __init__(self):

        self.knowledge_service = KnowledgeService()

    def execute(self, context):

        log_step(
            "[ORCHESTRATOR_ROUTE]",
            context.query_type
        )

        if context.query_type == "knowledge":

            return self.knowledge_service.answer(
                context.rewritten_query
            )

        elif context.query_type == "physiology":

            return "Physiology workflow not implemented yet"

        elif context.query_type == "recommendation":

            return "Recommendation workflow not implemented yet"

        raise Exception(
            f"Unsupported query type: {context.query_type}"
        )

