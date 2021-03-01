import os
from datetime import timedelta

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

app = Celery("server")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(worker_pool_restarts=True)
app.conf.timezone = "UTC"

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Add periodic tasks."""
    from apps.projects.tasks import (  # noqa: WPS433
        cleanup_couchdb_task,
        cleanup_project_assets_task,
    )

    sender.add_periodic_task(
        timedelta(hours=1),
        cleanup_couchdb_task.s(),
        name="cleanup couchdb",
    )

    sender.add_periodic_task(
        timedelta(days=1),
        cleanup_project_assets_task.s(),
        name="cleanup project assets",
    )
