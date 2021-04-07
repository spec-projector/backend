from datetime import timedelta

import pytest
from django.utils import timezone

from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import SubscriptionFactory
from tests.test_users.factories.user import UserFactory


def test_none(user, ghl_client, ghl_raw):
    """Test empty subscription."""
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    subscription_dto = response["data"]["me"]["subscription"]

    assert subscription_dto is None


def test_single_active(user, ghl_client, ghl_raw):
    """Test single active subscription."""
    subscription = SubscriptionFactory.create(
        user=user,
        status=SubscriptionStatus.ACTIVE,
    )
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    subscription_dto = response["data"]["me"]["subscription"]

    assert subscription_dto is not None
    assert int(subscription_dto["id"]) == subscription.id


@pytest.mark.parametrize(
    "status",
    [
        SubscriptionStatus.CONFIRMING,
        SubscriptionStatus.CANCELED,
        SubscriptionStatus.OPTION,
        SubscriptionStatus.EXPIRED,
    ],
)
def test_inactive(user, ghl_client, ghl_raw, status):
    """Test single active subscription."""
    SubscriptionFactory.create(user=user, status=status)
    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    subscription_dto = response["data"]["me"]["subscription"]

    assert subscription_dto is None


def test_many(user, ghl_client, ghl_raw):
    """Test many subscription."""
    SubscriptionFactory.create(
        created_at=timezone.now() - timedelta(days=1),
        user=user,
    )

    subscription = SubscriptionFactory.create(
        created_at=timezone.now(),
        user=user,
        status=SubscriptionStatus.ACTIVE,
    )

    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    subscription_dto = response["data"]["me"]["subscription"]

    assert subscription_dto is not None
    assert int(subscription_dto["id"]) == subscription.id


def test_many_inactive(user, ghl_client, ghl_raw):
    """Test many inactive subscription."""
    SubscriptionFactory.create(
        created_at=timezone.now() - timedelta(days=1),
        user=user,
    )

    SubscriptionFactory.create(
        created_at=timezone.now(),
        user=user,
    )

    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    subscription_dto = response["data"]["me"]["subscription"]

    assert subscription_dto is None


def test_another_user(user, ghl_client, ghl_raw):
    """Test another user active subscription."""
    another_user = UserFactory.create()
    SubscriptionFactory.create(
        user=another_user,
        status=SubscriptionStatus.ACTIVE,
    )

    ghl_client.set_user(user)

    response = ghl_client.execute(ghl_raw("me_subscription"))

    subscription_dto = response["data"]["me"]["subscription"]

    assert subscription_dto is None
