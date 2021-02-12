import pytest

from apps.core import injector
from apps.core.services.figma import IFigmaServiceFactory
from tests.helpers.figma import StubFigmaFactoryService


@pytest.fixture()
def figma_service():
    """Provides Figma mocked service."""
    service = StubFigmaFactoryService()
    injector.binder.bind(IFigmaServiceFactory, service)

    return service
