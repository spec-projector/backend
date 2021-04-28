import pytest

from apps.billing.logic.interfaces import (
    ISubscriptionService,
    ITariffLimitsService,
)
from apps.core import injector


@pytest.fixture()
def subscription_service():
    """Provides subscription service."""
    return injector.get(ISubscriptionService)


@pytest.fixture()
def tariff_limits_service():
    """Provides user tariff service."""
    return injector.get(ITariffLimitsService)
