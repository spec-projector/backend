import pytest

from apps.core import injector
from apps.core.services.couchdb import ICouchDBService
from tests.helpers.couchdb import StubCouchDBService


@pytest.fixture()  # delete
def couchdb_service():
    """Provides CouchDB mocked service."""
    service = StubCouchDBService()
    injector.binder.bind(ICouchDBService, service)

    return service
