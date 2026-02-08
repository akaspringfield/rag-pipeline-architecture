from common.logger import log_step
from query_processing.classifier import classify_query
from query_processing.query_context import QueryContext
from query_processing.rewriter import rewrite_query


class QueryService:

    def process(
        self,
        user_id: str,
        query: str
    ) -> QueryContext:

        query_type = classify_query(query)

        rewritten_query = rewrite_query(query)

        log_step("QUERY_TYPE", query_type)
        log_step("REWRITTEN_QUERY", rewritten_query)

        return QueryContext(
            user_id=user_id,
            query=query,
            query_type=query_type,
            rewritten_query=rewritten_query
        )