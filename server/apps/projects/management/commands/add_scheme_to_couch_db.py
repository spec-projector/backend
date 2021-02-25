from cloudant.document import Document
from django.core.management import BaseCommand

from apps.core import injector
from apps.core.logic.interfaces import ICouchDBService


class Command(BaseCommand):
    """Command update couchdb scheme."""

    def handle(self, *args, **options):  # noqa: WPS110
        """Handler."""
        couch_db = injector.get(ICouchDBService)
        for db_name in couch_db.list_databases():
            db = couch_db.get_database(db_name)
            with Document(db, "spec") as doc:
                doc["scheme"] = {"version": 1}
                doc.save()

        couch_db.close()
