from database.connection import (
    SessionLocal
)

from database.entities.ingestion_job_entity import (
    IngestionJobEntity
)

from database.models.ingestion_job import (
    IngestionJob
)


class IngestionJobRepository:

    def save(
        self,
        job: IngestionJob
    ):

        db = SessionLocal()

        try:

            entity = IngestionJobEntity(
                job_id=job.job_id,
                document_id=job.document_id,
                status=job.status,
                progress=job.progress,
                error_message=job.error_message,
                created_at=job.created_at
            )

            db.add(entity)

            db.commit()

            print(
                f"[JOB_SAVED] => "
                f"{job.job_id}"
            )

            return job

        finally:

            db.close()

    def update_status(
        self,
        job_id: str,
        status: str,
        progress: int
    ):

        print(
            f"[DB_UPDATE_ATTEMPT] "
            f"{job_id} -> {status}"
        )
        db = SessionLocal()

        try:

            entity = (
                db.query(
                    IngestionJobEntity
                )
                .filter(
                    IngestionJobEntity.job_id
                    == job_id
                )
                .first()
            )

            if entity:

                entity.status = status

                entity.progress = progress

                db.commit()
                print(
                    f"[DB_COMMIT_DONE] "
                    f"{job_id}"
                )
            return entity

        finally:

            db.close()



    def get(
        self,
        job_id: str
    ):

        db = SessionLocal()

        try:

            return (
                db.query(
                    IngestionJobEntity
                )
                .filter(
                    IngestionJobEntity.job_id
                    == job_id
                )
                .first()
            )

        finally:

            db.close()

    def mark_failed(
        self,
        job_id: str,
        error_message: str
    ):

        db = SessionLocal()

        try:

            entity = (
                db.query(
                    IngestionJobEntity
                )
                .filter(
                    IngestionJobEntity.job_id
                    == job_id
                )
                .first()
            )

            if entity:

                entity.status = "FAILED"

                entity.error_message = (
                    error_message
                )

                db.commit()

            return entity

        finally:

            db.close()