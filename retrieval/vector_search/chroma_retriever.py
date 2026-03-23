"""
Builds a merged retriever across all three Chroma collections:
  - faq     : FAQ entries
  - tickets : resolved support tickets
  - guides  : PDF guide chunks
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
    TOP_K_GUIDES,
    MIN_SIMILARITY_SCORE
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

    print("STEP 4")

    def retrieve(query: str) -> list[Document]:

        print(
            f"[RETRIEVE_QUERY] => {query}"
        )

        faq_docs = faq_store.similarity_search_with_score(
            query,
            k=k_faq
        )

        ticket_docs = tickets_store.similarity_search_with_score(
            query,
            k=k_tickets
        )

        guide_docs = guides_store.similarity_search_with_score(
            query,
            k=k_guides
        )

        results = (
            faq_docs
            + ticket_docs
            + guide_docs
        )

        docs = []

        for idx, (doc, score) in enumerate(results):

            print(
                f"[DOC_{idx+1}_SOURCE] => "
                f"{doc.metadata.get('source')}"
            )

            print(
                f"[DOC_{idx+1}_SCORE] => "
                f"{score}"
            )

            print(
                f"[DOC_{idx+1}_CONTENT] => "
                f"{doc.page_content[:150]}"
            )

            if score <= MIN_SIMILARITY_SCORE:

                docs.append(doc)

                print(
                    f"[DOC_{idx+1}] ACCEPTED"
                )

            else:

                print(
                    f"[DOC_{idx+1}] REJECTED"
                )

        print(
            f"[FINAL_DOC_COUNT] => {len(docs)}"
        )

        return docs

    return RunnableLambda(retrieve)