from apps.projects.services.project_asset.cleanup import cleanup_project_assets
from celery_app import app


@app.task
def cleanup_project_assets_task():
    """Cleanup project assets task."""
    cleanup_project_assets()
