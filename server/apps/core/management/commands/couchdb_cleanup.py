from django.core.management import BaseCommand

from apps.core import injector
from apps.core.services import CouchDBMaintenanceService


class Command(BaseCommand):
    """Run database compact."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Handler."""
        service = injector.get(CouchDBMaintenanceService)
        service.cleanup_databases(self.stdout)
