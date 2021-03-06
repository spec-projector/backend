from typing import List

from apps.core.logic.interfaces import ICouchDBService


class StubCouchDBService(ICouchDBService):
    """Mocked CouchDB service."""

    def __init__(self) -> None:
        """Initializing."""
        self.create_database_called = False
        self.delete_database_called = False
        self.deleted_db_names: List[str] = []

    def list_databases(self):
        """Get all database names."""
        return ["db-1", "db-2", "db-3"]

    def create_database(self, db_name: str):
        """Create database with provided name."""
        self.create_database_called = True

    def get_database(self, db_name: str):
        """Get database by id."""

    def delete_database(self, db_name: str) -> None:
        """Delete database with provided name."""
        self.delete_database_called = True
        self.deleted_db_names.append(db_name)

    def close(self) -> None:
        """Closes session."""
