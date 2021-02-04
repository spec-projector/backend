from django.core.management import BaseCommand

from apps.core import injector
from apps.core.services.couchdb import ICouchDBService


class Command(BaseCommand):
    """Command cleanup couchdb."""

    def add_arguments(self, parser):
        """Add arguments for current command."""
        parser.add_argument(
            "--dbname",
            type=str,
            dest="db_name",
            required=True,
        )

    def handle(self, *args, **options):  # noqa: WPS110
        """Cleanup couchdb."""
        couch_db = injector.get(ICouchDBService)
        couch_db.cleanup_database(options["db_name"])
        couch_db.close()
