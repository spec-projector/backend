from cloudant.database import CouchDatabase
from django.core.management import BaseCommand
from tqdm import tqdm

from apps.core import injector
from apps.core.logic.interfaces import ICouchDBService


class BaseDatabaseUpgradeCommand(BaseCommand):
    """Base upgrade couchdb scheme command ."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Handler."""
        couch_db = injector.get(ICouchDBService)
        for db_name in tqdm(couch_db.list_databases()):
            self.upgrade_database(couch_db.get_database(db_name))

        couch_db.close()

    def upgrade_database(self, db: CouchDatabase) -> None:
        """Upgrade database logic."""
        raise NotImplementedError()
