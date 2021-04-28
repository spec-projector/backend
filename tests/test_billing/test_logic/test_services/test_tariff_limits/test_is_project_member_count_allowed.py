import pytest

from apps.billing.logic.services.subscription import NoActiveSubscriptionError
from apps.billing.logic.services.tariff_limits import (
    MaxProjectMembersTariffError,
    NotFoundTariffError,
)
from apps.projects.models import Project
from tests.test_billing.factories import SubscriptionFactory
from tests.test_projects.factories import ProjectFactory


@pytest.fixture()
def project(user) -> Project:
    """Create project."""
    return ProjectFactory.create(owner=user)


def test_is_project_member_count_allowed_is_empty(
    project,
    tariff_limits_service,
):
    """Test validate max project members is empty."""
    SubscriptionFactory.create(
        user=project.owner,
        tariff__max_project_members=0,
    )

    assert (
        tariff_limits_service.is_project_member_count_allowed(project, 10)
        is None
    )


def test_is_project_member_count_allowed(project, tariff_limits_service):
    """Test validate max project members."""
    SubscriptionFactory.create(
        user=project.owner,
        tariff__max_project_members=4,
    )

    assert (
        tariff_limits_service.is_project_member_count_allowed(project, 4)
        is None
    )


def test_validate_not_active_subscription(project, tariff_limits_service):
    """Test validate not subscription."""
    with pytest.raises(NoActiveSubscriptionError):
        tariff_limits_service.is_project_member_count_allowed(project, 0)


def test_validate_not_tariff(project, tariff_limits_service):
    """Test validate not tariff."""
    SubscriptionFactory.create(user=project.owner, tariff=None)

    with pytest.raises(NotFoundTariffError):
        tariff_limits_service.is_project_member_count_allowed(project, 0)


def test_max_project_members_limit(project, tariff_limits_service):
    """Test max project members limit."""
    SubscriptionFactory.create(
        user=project.owner,
        tariff__max_project_members=1,
    )

    with pytest.raises(MaxProjectMembersTariffError, match="1"):
        tariff_limits_service.is_project_member_count_allowed(project, 2)
