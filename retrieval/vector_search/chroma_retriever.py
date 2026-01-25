"""
Builds a merged retriever across all three Chroma collections:
  - faq     : FAQ entries (no chunking — 1 row = 1 doc)
  - tickets : resolved support tickets (no chunking — 1 ticket = 1 doc)
  - guides  : PDF guide chunks (RecursiveCharacterTextSplitter applied at ingest)
"""
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from config.settings import (
    CHROMA_DIR,
    EMBED_MODEL,
    TOP_K_FAQ,
    TOP_K_TICKETS,
    TOP_K_GUIDES
)


def build_retriever(
    k_faq: int = TOP_K_FAQ,
    k_tickets: int = TOP_K_TICKETS,
    k_guides: int = TOP_K_GUIDES,
):
    print("STEP 1")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL
    )

    print("STEP 2")

    faq_store = Chroma(
        collection_name="faq",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    tickets_store = Chroma(
        collection_name="tickets",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    guides_store = Chroma(
        collection_name="guides",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    print("STEP 3")

    faq_retriever = faq_store.as_retriever(
        search_kwargs={"k": k_faq}
    )

    tickets_retriever = tickets_store.as_retriever(
        search_kwargs={"k": k_tickets}
    )

    guides_retriever = guides_store.as_retriever(
        search_kwargs={"k": k_guides}
    )

    print("STEP 4")

    def retrieve(query: str) -> list[Document]:
        # return ("SUCCESS: Retrieved documents for query: " + query,)
        return (
            faq_retriever.invoke(query)
            + tickets_retriever.invoke(query)
            + guides_retriever.invoke(query)
        )

    return RunnableLambda(retrieve)