import pytest


@pytest.fixture(scope="session")
def upload_user_avatar_mutation(ghl_mutations):
    """Upload user avatar mutation."""
    return ghl_mutations.fields["uploadUserAvatar"].resolver
