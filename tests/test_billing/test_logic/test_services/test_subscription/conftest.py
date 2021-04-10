import pytest

from apps.billing.logic.interfaces import ISubscriptionService
from apps.core import injector


@pytest.fixture()
def subscription_service():
    """Provides subscription service."""
    return injector.get(ISubscriptionService)
