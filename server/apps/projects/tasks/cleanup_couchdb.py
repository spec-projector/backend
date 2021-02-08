from apps.projects.services.projects.couchdb import cleanup_couch_databases
from celery_app import app


@app.task
def cleanup_couchdb_task() -> None:
    """Cleanup couchdb task."""
    cleanup_couch_databases()
