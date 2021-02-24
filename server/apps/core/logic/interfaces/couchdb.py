import abc
from typing import List

from cloudant.database import CouchDatabase


class ICouchDBService(abc.ABC):
    """CouchDb service interface."""

    @abc.abstractmethod
    def list_databases(self) -> List[str]:
        """Get all databases."""

    @abc.abstractmethod
    def create_database(self, db_name: str) -> CouchDatabase:
        """Create database with provided name."""

    @abc.abstractmethod
    def get_database(self, db_name: str) -> CouchDatabase:
        """Get database with provided name."""

    @abc.abstractmethod
    def delete_database(self, db_name: str) -> None:
        """Delete database with provided name."""

    @abc.abstractmethod
    def close(self) -> None:
        """Closes session."""
