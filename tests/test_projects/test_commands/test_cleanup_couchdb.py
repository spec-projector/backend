from django.core.management import call_command

from tests.test_projects.factories.project import ProjectFactory


def test_cleanup_couchdb(db, couchdb_service):
    """Test command 'cleanup_couchdb'."""
    ProjectFactory(db_name="db-1")

    call_command("cleanup_couchdb")

    assert set(couchdb_service.deleted_db_names) == {"db-2", "db-3"}
