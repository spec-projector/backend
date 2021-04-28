import pytest

from apps.billing.logic.services.subscription import NoActiveSubscriptionError
from apps.billing.logic.services.user_tariff import (
    MaxProjectMembersTariffError,
    NotFoundTariffError,
)
from tests.test_billing.factories import SubscriptionFactory


def test_validate_max_project_members_is_empty(user, user_tariff_service):
    """Test validate max project members is empty."""
    subscription = SubscriptionFactory.create(
        user=user,
        tariff__max_project_members=0,
    )

    assert (
        user_tariff_service.validate_max_project_members(subscription, 10)
        is None
    )


def test_validate_max_project_members(user, user_tariff_service):
    """Test validate max project members."""
    subscription = SubscriptionFactory.create(
        user=user,
        tariff__max_project_members=4,
    )

    assert (
        user_tariff_service.validate_max_project_members(subscription, 4)
        is None
    )


def test_validate_not_active_subscription(user, user_tariff_service):
    """Test validate not subscription."""
    with pytest.raises(NoActiveSubscriptionError):
        user_tariff_service.validate_max_project_members(None, 0)


def test_validate_not_tariff(user, user_tariff_service):
    """Test validate not tariff."""
    subscription = SubscriptionFactory.create(user=user, tariff=None)

    with pytest.raises(NotFoundTariffError):
        user_tariff_service.validate_max_project_members(subscription, 0)


def test_max_project_members_limit(user, user_tariff_service):
    """Test max project members limit."""
    subscription = SubscriptionFactory.create(
        user=user,
        tariff__max_project_members=1,
    )

    with pytest.raises(MaxProjectMembersTariffError):
        user_tariff_service.validate_max_project_members(subscription, 2)
