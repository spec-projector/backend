from apps.core.services.couchdb import ICouchDBService


class StubCouchDBService(ICouchDBService):
    """Mocked CouchDB service."""

    def __init__(self):
        """Initializing."""
        self.create_database_called = False

    def create_database(self, db_name: str):
        """Create database with provided name."""
        self.create_database_called = True

    def close(self) -> None:
        """Closes session."""
