import pytest

from apps.billing.logic.interfaces import (
    ISubscriptionService,
    IUserTariffService,
)
from apps.core import injector


@pytest.fixture()
def subscription_service():
    """Provides subscription service."""
    return injector.get(ISubscriptionService)


@pytest.fixture()
def user_tariff_service():
    """Provides user tariff service."""
    return injector.get(IUserTariffService)
