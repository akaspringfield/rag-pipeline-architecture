from langchain_core.documents import Document


class MetadataFilter:

    def filter(
        self,
        docs: list[Document],
        knowledge_base: str,
        tenant_id: str | None = None,
    ) -> list[Document]:

        filtered_docs = []

        for doc in docs:

            metadata = doc.metadata

            # Knowledge base must match
            if (
                metadata.get("knowledge_base")
                != knowledge_base
            ):
                continue

            scope = metadata.get(
                "knowledge_scope"
            )

            chunk_tenant = metadata.get(
                "tenant_id"
            )

            # Public/general document
            if scope == "general":
                filtered_docs.append(doc)
                continue

            # Tenant-specific document
            if (
                tenant_id is not None
                and chunk_tenant == tenant_id
            ):
                filtered_docs.append(doc)

        return filtered_docs