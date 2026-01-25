from rag_chain import build_chain


class KnowledgeService:

    def __init__(self):
        self.chain = None

    def get_chain(self):

        if self.chain is None:
            self.chain = build_chain()

        return self.chain

    def answer(self, query):

        print(
            f"[KNOWLEDGE_SERVICE_QUERY] => {query}"
        )

        chain = self.get_chain()

        answer = ""

        for chunk in chain.stream(query):
            answer += chunk

        return answer