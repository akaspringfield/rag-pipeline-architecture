from celery import Celery

celery_app  = Celery(
    "rag_platform",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["workers.tasks.ingestion_task"]
)

celery_app.conf.update(
    task_track_started=True
)