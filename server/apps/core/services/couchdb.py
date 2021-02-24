from contextlib import suppress
from typing import List

from cloudant import CouchDB
from cloudant.database import CouchDatabase
from cloudant.error import CloudantClientException
from constance import config

from apps.core.logic.interfaces import ICouchDBService


class CouchDBService(ICouchDBService):
    """CouchDb client."""

    def __init__(self):
        """Initialize."""
        self._client = CouchDB(
            config.COUCHDB_USER,
            config.COUCHDB_PASSWORD,
            url=config.COUCHDB_URL,
            connect=True,
            auto_renew=True,
        )

    def list_databases(self) -> List[str]:
        """Get all databases."""
        return self._client.all_dbs()

    def create_database(self, db_name: str) -> CouchDatabase:
        """Create database with provided name."""
        return self._client.create_database(db_name)

    def get_database(self, db_name: str) -> CouchDatabase:
        """Get database with provided name."""
        return self._client.get(db_name, remote=True)

    def delete_database(self, db_name: str) -> None:
        """Create database with provided name."""
        with suppress(CloudantClientException):
            self._client.delete_database(db_name)

    def close(self) -> None:
        """Closes session."""
        self._client.disconnect()
