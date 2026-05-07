class ReciprocalRankFusion:

    def fuse(
        self,
        result_lists,
        k: int = 60
    ):

        scores = {}

        for results in result_lists:

            for rank, doc in enumerate(results):

                key = (
                    doc.metadata.get("document_id"),
                    doc.metadata.get("chunk_index")
                )

                if key not in scores:

                    scores[key] = {
                        "doc": doc,
                        "score": 0.0
                    }

                scores[key]["score"] += (
                    1.0 / (k + rank + 1)
                )

        ranked = sorted(
            scores.values(),
            key=lambda item: item["score"],
            reverse=True
        )

        return [
            item["doc"]
            for item in ranked
        ]