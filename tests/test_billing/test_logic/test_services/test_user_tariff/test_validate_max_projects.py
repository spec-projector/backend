import pytest

from apps.billing.logic.services.user_tariff import (
    MaxProjectsTariffError,
    NotFoundTariffError,
)
from tests.test_billing.factories import SubscriptionFactory


def test_validate_max_projects_is_empty(user, user_tariff_service):
    """Test validate max projects is empty."""
    subscription = SubscriptionFactory.create(
        user=user,
        tariff__max_projects=0,
    )

    assert user_tariff_service.validate_max_projects(subscription, 10) is None


def test_validate_max_projects(user, user_tariff_service):
    """Test validate max projects."""
    subscription = SubscriptionFactory.create(
        user=user,
        tariff__max_projects=4,
    )

    assert user_tariff_service.validate_max_projects(subscription, 4) is None


def test_validate_not_tariff(user, user_tariff_service):
    """Test validate not tariff."""
    subscription = SubscriptionFactory.create(user=user, tariff=None)

    with pytest.raises(NotFoundTariffError):
        user_tariff_service.validate_max_projects(subscription, 1)


def test_max_projects_limit(user, user_tariff_service):
    """Test max projects limit."""
    subscription = SubscriptionFactory.create(
        user=user,
        tariff__max_projects=1,
    )

    with pytest.raises(MaxProjectsTariffError):
        user_tariff_service.validate_max_projects(subscription, 2)
