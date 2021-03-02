import pytest


@pytest.fixture(scope="session")
def reset_password_mutation(ghl_mutations):
    """
    Reset password mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["resetPassword"].resolver
