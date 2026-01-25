from services.knowledge_service import KnowledgeService


class SolutionOrchestrator:

    def __init__(self):

        self.knowledge_service = KnowledgeService()

    def execute(self, context):

        print(
            f"[ORCHESTRATOR_ROUTE] => {context.query_type}"
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

