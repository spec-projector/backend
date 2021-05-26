from cloudant.database import CouchDatabase
from cloudant.document import Document

from apps.core.management.commands.base_upgrade import (
    BaseDatabaseUpgradeCommand,
)


class Command(BaseDatabaseUpgradeCommand):
    """Command update couchdb scheme to v6."""

    def upgrade_database(self, db: CouchDatabase) -> None:
        """Upgrade database logic."""
        with Document(db, "spec") as spec_doc:
            if "epics" in spec_doc:  # noqa: WPS529
                del spec_doc["epics"]  # noqa: WPS420 WPS529

            if "packages" in spec_doc:
                self._clear_packages(db, spec_doc)
                del spec_doc["packages"]  # noqa: WPS420 WPS529

            spec_doc["scheme"] = {"version": 6}

            spec_doc.save()

    def _clear_packages(self, db: CouchDatabase, spec_doc: Document):
        packages = spec_doc.get("packages")
        if not packages:
            return

        for package in packages:
            with Document(db, package["_id"]) as package_doc:
                package_doc.delete()
