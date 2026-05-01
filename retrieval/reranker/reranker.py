from sentence_transformers import CrossEncoder


class Reranker:

    _model = None

    def __init__(self):

        if self.__class__._model is None:

            self.__class__._model = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

        self.model = self.__class__._model

    def rerank(
        self,
        query: str,
        docs: list,
        top_n: int = 5
    ):

        if not docs:
            return []

        pairs = [
            (
                query,
                doc.page_content
            )
            for doc in docs
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(
                docs,
                scores
            ),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, _ in ranked[:top_n]
        ]