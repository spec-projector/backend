import pytest

from tests.test_users.factories.user_access_token import UserAccessTokenFactory


@pytest.fixture(scope="session")
def add_access_token_mutation(ghl_mutations):
    """Add access token mutation."""
    return ghl_mutations.fields["addAccessToken"].resolver


@pytest.fixture()
def delete_access_token_mutation(ghl_mutations):
    """Delete access token mutation."""
    return ghl_mutations.fields["deleteAccessToken"].resolver


@pytest.fixture()
def user_access_token(user):
    """Create user access token."""
    return UserAccessTokenFactory.create(user=user)
