import abc
from contextlib import suppress
from typing import List

from cloudant import Cloudant
from cloudant.error import CloudantClientException
from constance import config

from apps.core import injector


class ICouchDBService(abc.ABC):
    """CouchDb service interface."""

    @abc.abstractmethod
    def list_databases(self) -> List[str]:
        """Get all databases."""

    @abc.abstractmethod
    def create_database(self, db_name: str):
        """Create database with provided name."""

    @abc.abstractmethod
    def delete_database(self, db_name: str) -> None:
        """Delete database with provided name."""

    @abc.abstractmethod
    def close(self) -> None:
        """Closes session."""


class CouchDBService(ICouchDBService):
    """CouchDb client."""

    def __init__(self):
        """Initialize."""
        self._client = Cloudant(
            config.COUCHDB_USER,
            config.COUCHDB_PASSWORD,
            url=config.COUCHDB_URL,
            connect=True,
            auto_renew=True,
        )

    def list_databases(self) -> List[str]:
        """Get all databases."""
        return self._client.all_dbs()

    def create_database(self, db_name: str):
        """Create database with provided name."""
        return self._client.create_database(db_name)

    def delete_database(self, db_name: str) -> None:
        """Create database with provided name."""
        with suppress(CloudantClientException):
            self._client.delete_database(db_name)

    def close(self) -> None:
        """Closes session."""
        self._client.disconnect()


def delete_couch_databases(db_names: List[str]) -> None:
    """Delete databases."""
    couch_db = injector.get(ICouchDBService)
    for db_name in db_names:
        couch_db.delete_database(db_name)

    couch_db.close()
