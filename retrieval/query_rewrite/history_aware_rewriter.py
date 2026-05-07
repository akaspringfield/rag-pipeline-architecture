from langchain_groq import ChatGroq

from config.settings import (
    LLM_MODEL,
)
import re


class HistoryAwareRewriter:

    def __init__(self):

        self.llm = ChatGroq(
            model=LLM_MODEL,
            temperature=0,
        )

    def rewrite(
        self,
        history: str,
        query: str,
    ) -> str:

        if not history.strip():
            return query

        prompt = f"""
            You are an expert query rewriting assistant.

            Given the conversation history and the latest user question,
            rewrite the latest question into a standalone question.

            Conversation:
            {history}

            Latest Question:
            {query}

            Return ONLY the rewritten question.
            Do NOT include explanations, reasoning, XML tags, markdown,
            or <think> blocks.
            """

        response = self.llm.invoke(prompt)

        rewritten = response.content.strip()

        # Remove reasoning if the model emits it
        rewritten = re.sub(
            r"<think>.*?</think>",
            "",
            rewritten,
            flags=re.DOTALL,
        ).strip()

        return rewritten