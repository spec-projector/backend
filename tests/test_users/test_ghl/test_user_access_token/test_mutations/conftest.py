import pytest


@pytest.fixture(scope="session")
def add_access_token_mutation(ghl_mutations):
    """Add access token mutation."""
    return ghl_mutations.fields["addAccessToken"].resolver
