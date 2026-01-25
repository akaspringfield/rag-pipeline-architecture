from retrieval.reranker.cross_encoder_reranker import rerank
from retrieval.vector_search.chroma_retriever import build_retriever
from common.exceptions import KnowledgeBaseEmptyException


class RetrievalService:

    def __init__(self):

        self.retriever = None

    def get_retriever(self):

        if self.retriever is None:

            print("[RETRIEVAL_SERVICE] Loading retriever")

            self.retriever = build_retriever()

        return self.retriever

    def retrieve(self, query):

        retriever = self.get_retriever()

        docs = retriever.invoke(query)

        print(
            f"[RETRIEVAL_DOC_COUNT] => {len(docs)}"
        )

        if len(docs) == 0:
            raise KnowledgeBaseEmptyException(
                "Knowledge base contains no documents"
            )

        for i, doc in enumerate(docs):

            print(
                f"[DOC {i+1}] "
                f"source={doc.metadata.get('source')} "
                f"text={doc.page_content[:100]}"
            )

        reranked_docs = rerank(
            query,
            docs
        )

        return reranked_docs
        # return docs
