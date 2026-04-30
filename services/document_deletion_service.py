from services.document_service import (
    DocumentService
)

from services.document_chunk_service import (
    DocumentChunkService
)

from services.storage_service import (
    StorageService
)

from ingestion.indexing.indexing_service import (
    IndexingService
)


class DocumentDeletionService:

    def delete_document(
        self,
        document_id: str,
        collection_name: str
    ):

        document = (
            DocumentService()
            .get(document_id)
        )

        if not document:

            return False

        DocumentChunkService().delete_document_chunks(
            document_id
        )

        IndexingService(
            collection_name
        ).delete_document(
            document_id
        )

        StorageService().delete(
            document.source_file
        )

        DocumentService().delete_document(
            document_id
        )

        return True