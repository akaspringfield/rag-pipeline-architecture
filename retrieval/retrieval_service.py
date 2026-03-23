from retrieval.vector_search.chroma_retriever import build_retriever
from retrieval.reranker.reranker import Reranker
from common.exceptions import KnowledgeBaseEmptyException
from common.logger import log_step
import time

class RetrievalService:

    def __init__(self):

        self.retriever = None
        self.reranker = Reranker()
    def get_retriever(self):

        if self.retriever is None:

            log_step(
                "RETRIEVAL_SERVICE",
                "Loading retriever"
            )

            self.retriever = build_retriever()

        return self.retriever

    def retrieve(self, query):

        retriever = self.get_retriever()

        start_time = time.time()

        docs = retriever.invoke(query)

        elapsed = round(
            time.time() - start_time,
            3
        )

        log_step(
            "[RETRIEVAL_DOC_COUNT]",
            len(docs)
        )
        
        unique_docs = []
        seen = set()

        for doc in docs:

            content = doc.page_content.strip()

            if content not in seen:

                seen.add(content)

                unique_docs.append(doc)

        docs = unique_docs

        log_step(
            "[DEDUP_DOC_COUNT]",
            len(docs)
        )

        log_step(
            "[RETRIEVAL_TIME_SECONDS]",
            elapsed
        )

        if len(docs) == 0:

            raise KnowledgeBaseEmptyException(
                "Knowledge base contains no documents"
            )

        for i, doc in enumerate(docs):

            log_step(
                f"DOC_{i+1}_SOURCE",
                doc.metadata.get("source")
            )

            log_step(
                f"DOC_{i+1}_CONTENT",
                doc.page_content[:150]
            )

        reranked_docs = self.reranker.rerank(
            query,
            docs
        )

        log_step(
            "RERANKED_DOC_COUNT",
            len(reranked_docs)
        )

        return reranked_docs