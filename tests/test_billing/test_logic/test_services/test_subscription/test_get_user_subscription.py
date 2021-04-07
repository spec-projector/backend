from datetime import timedelta

import pytest
from django.utils import timezone

from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import SubscriptionFactory
from tests.test_users.factories.user import UserFactory


def test_none(user, subscription_service):
    """Test empty subscription."""
    assert subscription_service.get_user_subscription(user) is None


def test_single_active(user, subscription_service):
    """Test single active subscription."""
    subscription = SubscriptionFactory.create(user=user)

    user_subscription = subscription_service.get_user_subscription(user)
    assert user_subscription is not None
    assert user_subscription.pk == subscription.pk


@pytest.mark.parametrize(
    "status",
    [
        SubscriptionStatus.PAST_DUE,
        SubscriptionStatus.CANCELED,
        SubscriptionStatus.REJECTED,
        SubscriptionStatus.EXPIRED,
    ],
)
def test_inactive(user, subscription_service, status):
    """Test single active subscription."""
    SubscriptionFactory.create(user=user, status=status)
    user_subscription = subscription_service.get_user_subscription(user)
    assert user_subscription is None


def test_many(user, subscription_service):
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

    user_subscription = subscription_service.get_user_subscription(user)
    assert user_subscription is not None
    assert user_subscription.pk == subscription.pk


def test_many_inactive(user, subscription_service):
    """Test many inactive subscription."""
    SubscriptionFactory.create(
        created_at=timezone.now() - timedelta(days=1),
        user=user,
        status=SubscriptionStatus.PAST_DUE,
    )

    SubscriptionFactory.create(
        created_at=timezone.now(),
        user=user,
        status=SubscriptionStatus.EXPIRED,
    )

    user_subscription = subscription_service.get_user_subscription(user)
    assert user_subscription is None


def test_another_user(user, subscription_service):
    """Test another user active subscription."""
    another_user = UserFactory.create()
    SubscriptionFactory.create(user=another_user)

    user_subscription = subscription_service.get_user_subscription(user)
    assert user_subscription is None
