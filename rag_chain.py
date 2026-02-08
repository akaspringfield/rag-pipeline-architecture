"""
Builds the RAG chain:

Query
 ↓
RetrievalService
 ↓
Prompt
 ↓
Groq LLM
 ↓
String Output
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_groq import ChatGroq

from retrieval.retrieval_service import RetrievalService
from langchain_core.runnables import RunnableLambda

SYSTEM_PROMPT = """
You are a helpful and professional general purpose assistant.

Your job is to help user's to resolve issues with their queries if solution is avaibale in DB.

Use ONLY the context below to answer the user's question.

The context comes from two sources:
- FAQ entries (general policy and how-to information)
- Past support tickets (real resolved cases with step-by-step resolutions)

If the context does not contain enough information to answer confidently,
say so clearly and suggest the user's to connect with support or browse our website.

Context:
{context}
"""
from config.settings import (
    LLM_MODEL,
    LLM_TEMPERATURE
)

def _format_docs(docs: list[Document]) -> str:

    sections = []

    for doc in docs:

        source = doc.metadata.get(
            "source",
            "unknown"
        ).upper()

        sections.append(
            f"[{source}]\n{doc.page_content}"
        )

    return "\n\n---\n\n".join(sections)


def build_chain():

    print("BUILD_CHAIN START")

    retrieval_service = RetrievalService()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{question}")
        ]
    )

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=None,
        reasoning_format="parsed",
        timeout=None,
        max_retries=2,
    )

    chain = (
        {
            "context":
                RunnableLambda(
                    retrieval_service.retrieve
                )
                | _format_docs,
            "question":
                RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    print("CHAIN CREATED")

    return chain