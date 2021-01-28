from cloudant import Cloudant
from constance import config


class CouchDBService:
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

    def create_database(self, db_name: str):
        """Create database with provided name."""
        return self._client.create_database(db_name)

    def close(self) -> None:
        """Closes session."""
        self._client.disconnect()
