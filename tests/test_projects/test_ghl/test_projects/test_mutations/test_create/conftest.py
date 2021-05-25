import pytest

from tests.test_billing.factories import SubscriptionFactory


@pytest.fixture()
def user(user):
    """Add subscription for user."""
    SubscriptionFactory.create(
        user=user,
        tariff__max_projects=0,
    )
    return user
