import pytest


@pytest.fixture(scope="session")
def upload_image_mutation(ghl_mutations):
    """Upload image mutation."""
    return ghl_mutations.fields["uploadImage"].resolver
