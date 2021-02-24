import pytest

from apps.core import injector
from apps.core.logic.interfaces import ICouchDBService
from tests.helpers.couchdb import StubCouchDBService


@pytest.fixture()
def couchdb_service():
    """Provides CouchDB mocked service."""
    service = StubCouchDBService()
    injector.binder.bind(ICouchDBService, service)

    return service
