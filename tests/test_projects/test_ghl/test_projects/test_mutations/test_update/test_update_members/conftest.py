import pytest

from tests.test_billing.factories import SubscriptionFactory
from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def user(user):
    """Add subscription for user."""
    SubscriptionFactory.create(
        user=user,
        tariff__max_project_members=0,
    )
    return user


@pytest.fixture()
def project(user):
    """Provides project."""
    return ProjectFactory.create(owner=user)
