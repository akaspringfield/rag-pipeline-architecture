from sentence_transformers import CrossEncoder
from config.settings import MIN_RERANK_SCORE


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

        best_score = max(scores)

        if best_score < MIN_RERANK_SCORE:

            print(
                "[LOW_CONFIDENCE_RETRIEVAL]"
            )

            return []

        print(
            f"[BEST_RERANK_SCORE] => {best_score}"
        )

        ranked = sorted(
            zip(docs, scores),
            key=lambda x: x[1],
            reverse=True
        )

        for idx, (_, score) in enumerate(ranked):

            print(
                f"[RERANK_{idx+1}_SCORE] => {score}"
            )

        return [
            doc
            for doc, score in ranked[:3]
        ]