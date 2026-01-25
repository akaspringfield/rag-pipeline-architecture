def rerank(query, docs):

    print(
        f"[RERANK_INPUT] => {len(docs)}"
    )

    reranked_docs = docs[:5]

    print(
        f"[RERANK_OUTPUT] => {len(reranked_docs)}"
    )

    return reranked_docs