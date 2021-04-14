import pytest


@pytest.fixture(scope="session")
def upload_me_avatar_mutation(ghl_mutations):
    """Upload me avatar mutation."""
    return ghl_mutations.fields["uploadMeAvatar"].resolver
