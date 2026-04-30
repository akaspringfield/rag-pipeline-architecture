def fuse(vector_docs, keyword_docs):
    merged = []

    seen = set()

    for doc in vector_docs + keyword_docs:

        if doc.page_content not in seen:

            merged.append(doc)

            seen.add(doc.page_content)

    return merged


class ReciprocalRankFusion:

    def fuse(
        self,
        result_lists,
        k: int = 60
    ):

        scores = {}

        for results in result_lists:

            for rank, doc in enumerate(results):

                content = doc.page_content

                if content not in scores:

                    scores[content] = {
                        "doc": doc,
                        "score": 0
                    }

                scores[content]["score"] += (
                    1 / (k + rank + 1)
                )

        ranked = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return [
            item["doc"]
            for item in ranked
        ]