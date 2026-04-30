from common.logger import log_step
from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query: str,
        docs: list
    ):

        if not docs:
            return []

        pairs = [
            (query, doc.page_content)
            for doc in docs
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        for idx, (_, score) in enumerate(ranked):

            log_step(
                f"RERANK_{idx+1}_SCORE",
                float(score)
            )

        final_docs = [
            doc
            for doc, score in ranked[:3]
        ]

        log_step(
            "FINAL_CONTEXT_DOCS",
            len(final_docs)
        )

        return final_docs