from services.document_service import (
    DocumentService
)

from services.ingestion_job_service import (
    IngestionJobService
)

from services.storage_service import (
    StorageService
)

from ingestion.hashing.file_hash_service import (
    FileHashService
)

from workers.tasks.ingestion_task import (
    process_document
)

from ingestion.metadata.document_type_service import (
    DocumentTypeService
)

from services.document_chunk_service import (
    DocumentChunkService
)

class IngestionService:

    def __init__(self):

        self.document_service = (
            DocumentService()
        )

        self.job_service = (
            IngestionJobService()
        )
        
        self.chunk_service = (
            DocumentChunkService()
        )

    def ingest(
        self,
        file_path: str,
        collection_name: str
    ):

        storage_path = (
            StorageService()
            .save(file_path)
        )

        print(
            f"[STORAGE_PATH] => "
            f"{storage_path}"
        )

        file_hash = (
            FileHashService()
            .generate(storage_path)
        )

        existing_document = (
            self.document_service
            .find_by_hash(file_hash)
        )

        if existing_document:

            print(
                "[DUPLICATE_DOCUMENT_FOUND]"
            )

            print(
                f"[EXISTING_DOCUMENT_ID] => "
                f"{existing_document.document_id}"
            )

            return {
                "document": existing_document,
                "duplicate": True
            }

        print(
            f"[FILE_HASH] => "
            f"{file_hash}"
        )

        document = (
            self.document_service.create_document(
                source_file=storage_path,
                file_hash=file_hash,
                knowledge_base="physiology",
                knowledge_scope="general",
                owner_type="admin",
                document_type=(
                    DocumentTypeService()
                    .detect(storage_path)
                ),
                tenant_id=None
            )
        )

        print(
            f"[DOCUMENT_ID] => "
            f"{document.document_id}"
        )

        job = (
            self.job_service.create_job(
                document.document_id
            )
        )

        print(
            f"[JOB_ID] => "
            f"{job.job_id}"
        )

        process_document.delay(
            file_path=storage_path,
            collection_name=collection_name,
            document_id=document.document_id,
            job_id=job.job_id,
            knowledge_base=document.knowledge_base,
            knowledge_scope=document.knowledge_scope,
            owner_type=document.owner_type,
            tenant_id=document.tenant_id
        )

        print(
            "[JOB_QUEUED]"
        )

        return {
            "document_id": document.document_id,
            "job_id": job.job_id,
            "status": "UPLOADED"
        }
    