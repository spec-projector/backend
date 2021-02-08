from apps.core.services.couchdb_databases import cleanup_couch_databases
from celery_app import app


@app.task
def cleanup_couchdb_task() -> None:
    """Cleanup couchdb task."""
    cleanup_couch_databases()
