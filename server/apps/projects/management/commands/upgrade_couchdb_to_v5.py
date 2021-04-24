from typing import List, Tuple

from cloudant.database import CouchDatabase
from cloudant.document import Document
from django.utils.baseconv import BASE62_ALPHABET
from django.utils.crypto import get_random_string

from apps.projects.management.commands.base_upgrade import (
    BaseDatabaseUpgradeCommand,
)


class Command(BaseDatabaseUpgradeCommand):
    """Command update couchdb scheme to v5."""

    def upgrade_database(self, db: CouchDatabase) -> None:
        """Upgrade database logic."""
        with Document(db, "spec") as doc:
            epics = doc.get("epics")
            if epics:
                doc["modules"] = epics

            if "packages" in doc:
                model_doc = self._generate_model_doc(db, doc)
                doc["model"] = model_doc["_id"]

            doc["scheme"] = {"version": 5}

            doc.save()

    def _generate_model_doc(
        self,
        db: CouchDatabase,
        spec_doc: Document,
    ) -> Document:
        doc_data = {
            "_id": get_random_string(8, BASE62_ALPHABET),
        }

        packages = spec_doc.get("packages")
        if packages:
            self._fill_model_data_from_packages(db, doc_data, packages)

        return db.create_document(doc_data)

    def _fill_model_data_from_packages(
        self,
        db: CouchDatabase,
        model_data,
        packages,
    ):
        model_entities = []
        model_enums = []
        for package in packages:
            entities, enums = self._extract_model_data(db, package["_id"])
            if entities:
                model_entities.extend(entities)
            if enums:
                model_enums.extend(enums)

        model_data["entities"] = model_entities
        model_data["enums"] = model_enums

    def _extract_model_data(
        self,
        db: CouchDatabase,
        package_id: str,
    ) -> Tuple[List[str], List[str]]:
        with Document(db, package_id) as package_doc:
            pack_entities = package_doc.get("entities")
            pack_enums = package_doc.get("enums")

            return pack_entities, pack_enums
