import pytest


@pytest.fixture()
def command_data():
    """Create register command."""
    return {
        "first_name": "new user",
        "email": "new_user@mail.net",
        "last_name": "newuser",
        "password": "123456",
    }
