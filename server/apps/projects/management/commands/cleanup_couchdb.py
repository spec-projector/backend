from django.core.management import BaseCommand

from apps.projects.services.projects.couchdb import cleanup_couch_databases


class Command(BaseCommand):
    """Command cleanup couchdb."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Cleanup couchdb."""
        cleanup_couch_databases()
        self.stdout.write("Cleanup is success.")
