from rag_chain import build_chain
from common.logger import log_step


class KnowledgeService:

    def __init__(self):
        self.chain = None

    def get_chain(self):

        if self.chain is None:
            self.chain = build_chain()

        return self.chain

    def answer(self, query,retrieval_profile="default"):

        log_step(
            "[KNOWLEDGE_SERVICE_QUERY]",
            query
        )

        log_step(
            "[RETRIEVAL_PROFILE]",
            retrieval_profile
        )

        chain = self.get_chain()

        answer = ""

        for chunk in chain.stream(query):
            answer += chunk

        return answer