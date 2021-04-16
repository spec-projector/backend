from typing import Generator

import pytest

from apps.billing.models import Subscription, Tariff
from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import TariffFactory


@pytest.fixture()
def default_tariff(override_config) -> Tariff:
    """Create default tariff."""
    return TariffFactory.create()


@pytest.fixture()
def default_tariff_config(  # noqa: PT004
    override_config,
    default_tariff,
) -> Generator[None, None, None]:
    """Add default tariff to config."""
    with override_config(
        DEFAULT_TARIFF=default_tariff,
    ):
        yield


def test_add(
    user,
    subscription_service,
    default_tariff_config,
    default_tariff,
):
    """Test add."""
    subscription_service.add_default_subscription(user)

    subscription = Subscription.objects.filter(
        user=user,
        tariff=default_tariff,
    ).first()
    assert subscription is not None
    assert subscription.active_until is None
    assert subscription.status == SubscriptionStatus.ACTIVE


def test_no_default(user, subscription_service):
    """Test no default."""
    TariffFactory.create()

    subscription_service.add_default_subscription(user)

    assert not Subscription.objects.filter(user=user).exists()


def test_inactive_default(
    user,
    subscription_service,
    default_tariff_config,
    default_tariff,
):
    """Test inactive default."""
    default_tariff.is_active = False
    default_tariff.save()

    subscription_service.add_default_subscription(user)

    assert not Subscription.objects.filter(user=user).exists()


def test_no_tariffs(user, subscription_service):
    """Test no any tariffs."""
    subscription_service.add_default_subscription(user)

    assert not Subscription.objects.filter(user=user).exists()
