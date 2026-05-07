from rank_bm25 import BM25Okapi


class BM25Index:

    _instance = None

    def __init__(self):
        self.bm25 = None
        self.documents = []
        self.is_loaded = False

    @classmethod
    def get_instance(cls):

        if cls._instance is None:
            cls._instance = BM25Index()

        return cls._instance

    def build(self, documents):

        self.documents = documents

        corpus = [
            doc.page_content.lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(corpus)

        self.is_loaded = True

    def search(
        self,
        query,
        top_k=20
    ):

        if self.bm25 is None:
            return []

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, _
            in ranked[:top_k]
        ]