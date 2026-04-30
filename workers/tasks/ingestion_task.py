from workers.celery_app import (
    celery_app
)

from ingestion.loaders.loader_factory import (
    LoaderFactory
)

from ingestion.chunking.chunking_service import (
    ChunkingService
)

from ingestion.metadata.metadata_service import (
    MetadataService
)

from ingestion.indexing.indexing_service import (
    IndexingService
)

from services.ingestion_job_service import (
    IngestionJobService
)

from services.document_service import (
    DocumentService
)

from services.document_chunk_service import (
    DocumentChunkService
)


@celery_app .task(name="workers.tasks.ingestion_task.process_document")
def process_document(
    file_path,
    collection_name,
    document_id,
    job_id,
    knowledge_base,
    knowledge_scope,
    owner_type,
    tenant_id
):

    try:

        job_service = IngestionJobService()

        job_service.update_status(
            job_id,
            "PROCESSING",
            10
        )

        loader = LoaderFactory.get_loader(
            file_path
        )

        docs = loader.load()

        job_service.update_status(
            job_id,
            "PROCESSING",
            30
        )

        chunks = (
            ChunkingService()
            .chunk(docs)
        )

        metadata = (
            MetadataService()
            .extract(
                file_path=file_path,
                knowledge_base=knowledge_base,
                knowledge_scope=knowledge_scope,
                owner_type=owner_type,
                tenant_id=tenant_id
            )
        )

        metadata["document_id"] = (
            document_id
        )

        for chunk in chunks:

            chunk.metadata.update(
                metadata
            )

        DocumentChunkService().save_chunks(
            document_id=document_id,
            chunks=chunks,
            knowledge_base=knowledge_base,
            knowledge_scope=knowledge_scope,
            owner_type=owner_type,
            tenant_id=tenant_id
        )


        job_service.update_status(
            job_id,
            "INDEXING",
            70
        )

        IndexingService(
            collection_name
        ).index(chunks)

        DocumentService().update_status(
            document_id,
            "READY"
        )

        job_service.update_status(
            job_id,
            "READY",
            100
        )

    except Exception as e:
        
        DocumentService().update_status(
                document_id,
                "FAILED"
            )

        job_service.mark_failed(
            job_id,
            str(e)
        )

        raise Exception(str(e))