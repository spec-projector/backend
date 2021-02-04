from apps.core import injector
from apps.core.services.couchdb import ICouchDBService


def test_cleanup_db(couchdb_service):
    """Test cleanup db."""
    assert not couchdb_service.create_database_called
    assert not couchdb_service.delete_database_called

    couch_db = injector.get(ICouchDBService)
    couch_db.cleanup_database("db_name")
    couch_db.close()

    assert couchdb_service.create_database_called
    assert couchdb_service.delete_database_called
