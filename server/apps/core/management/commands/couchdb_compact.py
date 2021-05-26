from django.core.management import BaseCommand
from tqdm import tqdm

from apps.core import injector
from apps.core.logic.interfaces import ICouchDBService


class Command(BaseCommand):
    """Run database compact."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Handler."""
        couch_db = injector.get(ICouchDBService)
        for db_name in tqdm(couch_db.list_databases()):
            db = couch_db.get_database(db_name)
            response = db.r_session.post(
                "{0}/_compact".format(db.database_url),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

        couch_db.close()
