import pytest


@pytest.fixture(scope="session")
def change_password_mutation(ghl_mutations):
    """
    Change password mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["changePassword"].resolver
