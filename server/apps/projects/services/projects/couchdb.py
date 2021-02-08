from apps.core import injector
from apps.core.services.couchdb import ICouchDBService
from apps.projects.models import Project


def cleanup_couch_databases() -> None:
    """Cleanup couch databases."""
    couch_db = injector.get(ICouchDBService)

    for_delete = set(couch_db.list_databases()) - set(
        Project.objects.values_list("db_name", flat=True),
    )

    for delete_db_name in for_delete:
        couch_db.delete_database(delete_db_name)

    couch_db.close()
