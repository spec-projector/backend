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
            self._upgrade_db(couch_db.get_database(db_name))

        couch_db.close()

    def _upgrade_db(self, db):
        with Document(db, "spec") as doc:
            packages = doc.get("packages")
            if packages:
                for package in packages:
                    self._update_package(db, package["_id"])

            doc["scheme"] = {"version": 2}
            if "integration" in doc:
                del doc["integration"]  # noqa: WPS420 WPS529

            doc.save()

    def _update_package(self, db, package_id):
        with Document(db, package_id) as doc:
            entities = doc.get("entities")
            if not entities:
                return

            for entity in entities:
                self._update_entity(db, entity["_id"])

    def _update_entity(self, db, entity_id):
        with Document(db, entity_id) as doc:
            fields = doc.get("fields")
            if not fields:
                return

            for field in fields:
                if field["type"] == "array":
                    field["type"] = "reference"
                    field["isArray"] = True

            doc.save()
