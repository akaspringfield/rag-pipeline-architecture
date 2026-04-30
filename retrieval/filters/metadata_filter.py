from langchain_core.documents import Document


class MetadataFilter:

    def filter(
        self,
        docs: list[Document],
        tenant_id: str,
        knowledge_base: str
    ):

        filtered = []

        for doc in docs:

            scope = doc.metadata.get(
                "knowledge_scope"
            )

            doc_tenant = doc.metadata.get(
                "tenant_id"
            )

            kb = doc.metadata.get(
                "knowledge_base"
            )

            if kb != knowledge_base:
                continue

            if scope == "general":
                filtered.append(doc)

            elif (
                scope == "private"
                and doc_tenant == tenant_id
            ):
                filtered.append(doc)

        return filtered