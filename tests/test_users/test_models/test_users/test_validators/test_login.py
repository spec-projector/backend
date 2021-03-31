import pytest
from django.core.exceptions import ValidationError

from apps.users.models.validators import LoginValidator


@pytest.fixture()
def validator():
    """Create login validator."""
    return LoginValidator()


@pytest.mark.parametrize(
    "login",
    [
        "123456",
        "username",
        "user__12",
        "user.user",
        "user-user",
        "--__--__",
        "user.first_name",
    ],
)
def test_success(validator, login):
    """Test valid logins."""
    assert validator(login) is None


@pytest.mark.parametrize(
    "login",
    [
        "12345",
        "User-user",
        "user%user",  # noqa: WPS323
        "user-user?",
        "123456abcdefghij",
        "",
        "user@mail.com",
        "{{ user.first_name }}",
    ],
)
def test_failed(validator, login):
    """Test not valid logins."""
    with pytest.raises(ValidationError):
        validator(login)
