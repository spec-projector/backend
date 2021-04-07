import pytest

from apps.billing.logic.services import SubscriptionService
from apps.core import injector


@pytest.fixture()
def subscription_service():
    """Provides subscription service."""
    return injector.get(SubscriptionService)
