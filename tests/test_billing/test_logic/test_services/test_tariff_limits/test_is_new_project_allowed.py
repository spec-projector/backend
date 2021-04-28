import pytest

from apps.billing.logic.services.tariff_limits import (
    MaxProjectsTariffError,
    NotFoundTariffError,
)
from tests.test_billing.factories import SubscriptionFactory
from tests.test_projects.factories import ProjectFactory


def test_validate_max_projects_is_empty(user, tariff_limits_service):
    """Test validate max projects is empty."""
    SubscriptionFactory.create(
        user=user,
        tariff__max_projects=0,
    )

    assert tariff_limits_service.is_new_project_allowed(user) is None


def test_is_new_project_allowed(user, tariff_limits_service):
    """Test validate max projects."""
    ProjectFactory.create_batch(3, owner=user)
    SubscriptionFactory.create(
        user=user,
        tariff__max_projects=4,
    )

    assert tariff_limits_service.is_new_project_allowed(user) is None


def test_validate_not_tariff(user, tariff_limits_service):
    """Test validate not tariff."""
    SubscriptionFactory.create(user=user, tariff=None)

    with pytest.raises(NotFoundTariffError):
        tariff_limits_service.is_new_project_allowed(user)


def test_max_projects_limit(user, tariff_limits_service):
    """Test max projects limit."""
    ProjectFactory.create(owner=user)
    SubscriptionFactory.create(
        user=user,
        tariff__max_projects=1,
    )

    with pytest.raises(MaxProjectsTariffError, match="1"):
        tariff_limits_service.is_new_project_allowed(user)
