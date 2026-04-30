from langchain_community.retrievers import BM25Retriever


class KeywordRetriever:

    def build(
        self,
        docs
    ):

        retriever = BM25Retriever.from_documents(
            docs
        )

        retriever.k = 5

        return retriever