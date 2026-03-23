def fuse(vector_docs, keyword_docs):
    merged = []

    seen = set()

    for doc in vector_docs + keyword_docs:

        if doc.page_content not in seen:

            merged.append(doc)

            seen.add(doc.page_content)

    return merged