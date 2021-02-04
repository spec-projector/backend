from apps.core import injector
from apps.core.services.couchdb import ICouchDBService


def test_delete_db(couchdb_service):
    """Test delete db."""
    assert not couchdb_service.delete_database_called

    couch_db = injector.get(ICouchDBService)
    couch_db.delete_database("db_name")
    couch_db.close()

    assert couchdb_service.delete_database_called
