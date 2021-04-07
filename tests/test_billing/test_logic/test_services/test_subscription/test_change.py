import pytest

from apps.billing.logic.services.subscription import SameTariffChangeError
from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import (
    ChangeSubscriptionRequestFactory,
    SubscriptionFactory,
    TariffFactory,
)


@pytest.fixture()
def change_request(user):
    """Returns change request."""
    return ChangeSubscriptionRequestFactory.create(
        user=user,
        tariff=TariffFactory.create(),
    )


def test_new(user, change_request, subscription_service):
    """Test new subscription."""
    subscription_service.change_user_subscription(change_request)

    subscription = Subscription.objects.filter(user=user).first()
    assert subscription is not None
    assert subscription.tariff == change_request.tariff
    assert subscription.status == SubscriptionStatus.ACTIVE

    change_request.refresh_from_db()
    assert change_request.from_subscription is None
    assert change_request.to_subscription == subscription


def test_deactivate_old(user, change_request, subscription_service):
    """Test deactivate old."""
    old_subscription = SubscriptionFactory.create(
        user=user,
        tariff=TariffFactory.create(),
    )
    subscription_service.change_user_subscription(change_request)

    old_subscription.refresh_from_db()
    assert old_subscription.status == SubscriptionStatus.CANCELED

    subscription = (
        Subscription.objects.exclude(pk=old_subscription.pk)
        .filter(user=user)
        .first()
    )
    assert subscription is not None
    assert subscription.tariff == change_request.tariff

    change_request.refresh_from_db()
    assert change_request.from_subscription == old_subscription
    assert change_request.to_subscription == subscription


def test_inactive_old(user, change_request, subscription_service):
    """Test inactive old."""
    old_subscription = SubscriptionFactory.create(
        user=user,
        tariff=TariffFactory.create(),
        status=SubscriptionStatus.CANCELED,
    )
    subscription_service.change_user_subscription(change_request)

    old_subscription.refresh_from_db()
    assert old_subscription.status == SubscriptionStatus.CANCELED

    subscription = (
        Subscription.objects.exclude(pk=old_subscription.pk)
        .filter(user=user)
        .first()
    )
    assert subscription is not None
    assert subscription.tariff == change_request.tariff


def test_same_tariff(user, change_request, subscription_service):
    """Test same tariff."""
    SubscriptionFactory.create(
        user=user,
        tariff=change_request.tariff,
    )

    with pytest.raises(SameTariffChangeError):
        subscription_service.change_user_subscription(change_request)

    assert Subscription.objects.count() == 1
