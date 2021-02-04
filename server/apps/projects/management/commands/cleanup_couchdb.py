from django.core.management import BaseCommand

from apps.core import injector
from apps.core.services.couchdb import ICouchDBService
from apps.projects.models import Project


class Command(BaseCommand):
    """Command cleanup couchdb."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Cleanup couchdb."""
        couch_db = injector.get(ICouchDBService)

        for_delete = set(couch_db.list_databases()) - set(
            Project.objects.values_list("db_name", flat=True),
        )

        for delete_db_name in for_delete:
            couch_db.delete_database(delete_db_name)

        couch_db.close()
