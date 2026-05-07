"""
Expected:

Chroma retrieves relevant chunks.
BM25 also finds matches.
RRF combines them.
CrossEncoder orders them.
LLM answers correctly.
"""
import time

from common.exceptions import KnowledgeBaseEmptyException
from common.logger import log_step

from retrieval.vector_search.chroma_retriever import build_retriever
from retrieval.filters.metadata_filter import MetadataFilter
from retrieval.reranker.reranker import Reranker

from config.settings import *

class RetrievalService:

    def __init__(self):
        self.retriever = None
        self.metadata_filter = MetadataFilter()
        self.reranker = Reranker()


    def get_retriever(
        self,
        top_k: int
    ):
        if self.retriever is None:

            log_step(
                "RETRIEVAL_SERVICE",
                "Loading retriever"
            )

            return build_retriever(
                collection_name="default",
                top_k=TOP_K
            )

        return self.retriever

    def retrieve(
        self,
        query: str,
        knowledge_base: str,
        tenant_id: str | None = None,
        conversation_id: str | None = None,
        top_k: int = TOP_K,
    ):

        start_time = time.time()

        retriever = self.get_retriever(
            top_k=top_k
        )

        # Step 1: vector retrieval
        docs = retriever.invoke(query)

        # Step 2: metadata filtering
        docs = self.metadata_filter.filter(
            docs=docs,
            tenant_id=tenant_id,
            knowledge_base=knowledge_base,
        )

        # Step 3: deduplicate
        unique_docs = []
        seen = set()

        for doc in docs:

            document_id = doc.metadata.get("document_id")
            chunk_index = doc.metadata.get("chunk_index")

            key = (document_id, chunk_index)

            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)

        docs = unique_docs

        log_step(
            "FILTERED_DOC_COUNT",
            len(docs)
        )

        if len(docs) == 0:
            raise KnowledgeBaseEmptyException(
                "Knowledge base contains no matching documents."
            )

        log_step(
            "RERANK_INPUT_COUNT",
            len(docs)
        )

        # Step 4: rerank
        reranked_docs = self.reranker.rerank(
            query,
            docs
        )

        log_step(
            "RERANK_OUTPUT_COUNT",
            len(reranked_docs)
        )

        elapsed = round(
            time.time() - start_time,
            3
        )

        log_step(
            "FINAL_DOC_COUNT",
            len(reranked_docs)
        )

        log_step(
            "RETRIEVAL_TIME_SECONDS",
            elapsed
        )

        return reranked_docs
    
    def extract_sources(self, docs):

        sources = []

        seen = set()

        for doc in docs:

            source = {
                "document_id": doc.metadata.get(
                    "document_id"
                ),
                "chunk_index": doc.metadata.get(
                    "chunk_index"
                ),
                "source": doc.metadata.get(
                    "source"
                )
            }

            key = (
                source["document_id"],
                source["chunk_index"]
            )

            if key not in seen:

                seen.add(key)

                sources.append(source)

        return sources