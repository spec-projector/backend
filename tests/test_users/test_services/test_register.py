import pytest

from apps.users.models import User
from apps.users.services.register import (
    RegistrationInputError,
    RegistrationService,
    UserAlreadyExistsError,
)

LOGIN = "newuser"
EMAIL = "new_user@mail.net"


@pytest.fixture()
def register_data(db):
    """Create register data for new user."""
    return {
        "name": "new user",
        "email": EMAIL,
        "login": LOGIN,
        "password": "123456",
    }


def test_register_success(register_data):
    """Test success register."""
    service = RegistrationService()
    user = service.register(**register_data)

    _assert_user(user, register_data)
    assert user.is_active


@pytest.mark.parametrize(
    ("user_field", "field_value"),
    [
        ("login", LOGIN),
        ("email", EMAIL),
    ],
)
def test_exists_user(user, register_data, user_field, field_value):
    """Test exists_login. Not create new users."""
    setattr(user, user_field, field_value)
    user.save()

    with pytest.raises(UserAlreadyExistsError):
        RegistrationService().register(**register_data)

    assert User.objects.count() == 1


@pytest.mark.parametrize(
    ("field", "field_value"),
    [
        ("name", "a" * 51),
        ("login", "b" * 21),
        ("email", "{0}@net.com".format("c" * 50)),
        ("email", "wrong_email"),
    ],
)
def test_wrong_input_data(register_data, field, field_value):
    """Test wrong input. Wrong lengths from User - model."""
    register_data[field] = field_value

    with pytest.raises(RegistrationInputError):
        RegistrationService().register(**register_data)


def _assert_user(user, register_data) -> None:
    """Assert user."""
    assert user.name == register_data["name"]
    assert user.email == register_data["email"]
    assert user.login == register_data["login"]
    assert user.password
