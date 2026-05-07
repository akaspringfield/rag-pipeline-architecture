from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from retrieval.retrieval_service import RetrievalService
from prompts.knowledge_prompt import SYSTEM_PROMPT
from services.chat_service import ChatService

from retrieval.query_rewrite.history_builder import (
    HistoryBuilder
)
from retrieval.query_rewrite.history_aware_rewriter import (
    HistoryAwareRewriter
)
from common.exceptions import (
    KnowledgeBaseEmptyException
)
from config.settings import (
    LLM_MODEL,
    LLM_TEMPERATURE,
)

from common.logger import log_step


class KnowledgeService:

    def __init__(self):

        self.chat_service = ChatService()

        self.rewriter = HistoryAwareRewriter()
        self.retrieval_service = RetrievalService()

        self.llm = ChatGroq(
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=None,
            reasoning_format="parsed",
            timeout=None,
            max_retries=2,
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("human", "{question}"),
            ]
        )

    def _format_docs(self, docs):

        sections = []

        for doc in docs:

            source = doc.metadata.get(
                "source",
                "unknown"
            ).upper()

            sections.append(
                f"[{source}]\n{doc.page_content}"
            )

        return "\n\n---\n\n".join(sections)

    def answer(
        self,
        query: str,
        knowledge_base: str,
        tenant_id: str | None = None,
        session_id=None,
    ):

        rewritten_query = query

        if session_id:

            messages = (
                self.chat_service.get_messages(
                    session_id
                )
            )

            history = (
                HistoryBuilder.build(
                    messages
                )
            )

            rewritten_query = (
                self.rewriter.rewrite(
                    history=history,
                    query=query,
                )
            )

        log_step(
            "KNOWLEDGE_QUERY",
            query,
        )

        try:
            docs = self.retrieval_service.retrieve(
                query=query,
                knowledge_base=knowledge_base,
                tenant_id=tenant_id,
                conversation_id=None,
            )
        except KnowledgeBaseEmptyException:

            return (
                "I couldn't find any relevant information "
                "in the knowledge base to answer your question."
            )
        context = self._format_docs(docs)

        messages = self.prompt.invoke(
            {
                "context": context,
                "question": query,
            }
        )

        response = self.llm.invoke(messages)

        log_step("ORIGINAL_QUERY", query)
        log_step("REWRITTEN_QUERY", rewritten_query)

        return response.content