import pytest

from tests.test_billing.factories import SubscriptionFactory
from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project():
    """Provides project."""
    return ProjectFactory.create()


@pytest.fixture()
def user(user):
    """Add subscription for user."""
    SubscriptionFactory.create(
        user=user,
        tariff__max_project_members=0,
    )
    return user
