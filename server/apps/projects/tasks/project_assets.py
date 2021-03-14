from apps.core import injector
from apps.projects.services import ProjectAssetCleanupService
from celery_app import app


@app.task
def cleanup_project_assets_task():
    """Cleanup project assets task."""
    injector.get(ProjectAssetCleanupService).cleanup()
