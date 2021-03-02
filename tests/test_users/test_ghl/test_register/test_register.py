from typing import Dict

import pytest

from apps.core import injector
from apps.users.logic.interfaces import IAuthenticationService
from apps.users.models import Token, User
from apps.users.services.register import UserAlreadyExistsError
from tests.fixtures.users import DEFAULT_USER_PASSWORD, DEFAULT_USERNAME

EMAIL = "new_user@mail.net"


def test_query(db, ghl_client, ghl_raw):
    """Test register raw query."""
    assert not User.objects.filter(email=EMAIL).exists()

    register_data = _get_register_data()
    response = ghl_client.execute(
        ghl_raw("register"),
        variable_values={
            "input": register_data,
        },
    )

    assert "errors" not in response

    user = User.objects.get(email=EMAIL)
    token = Token.objects.get(user=user)

    assert response["data"]["register"]["token"]["key"] == token.key
    _check_auth(register_data["login"], register_data["password"])


def test_success(db, ghl_mock_info, register_mutation):
    """Test success register."""
    assert not User.objects.filter(email=EMAIL).exists()

    register_data = _get_register_data()
    response = register_mutation(
        root=None,
        info=ghl_mock_info,
        input=register_data,
    )

    assert Token.objects.get(pk=response.token.pk, user__email=EMAIL)
    _check_auth(register_data["login"], register_data["password"])


@pytest.mark.parametrize(
    ("user_field", "field_value"),
    [
        ("login", DEFAULT_USERNAME),
        ("email", EMAIL),
    ],
)
def test_wrong_register(
    user,
    register_mutation,
    ghl_mock_info,
    user_field,
    field_value,
):
    """Test exists user."""
    setattr(user, user_field, field_value)
    user.save()

    register_data = _get_register_data()
    with pytest.raises(UserAlreadyExistsError):
        register_mutation(
            root=None,
            info=ghl_mock_info,
            input=register_data,
        )

    assert User.objects.count() == 1


def _check_auth(username, password) -> None:
    """Check success auth after register user."""
    auth = injector.get(IAuthenticationService)
    assert auth.auth(username, password)


def _get_register_data() -> Dict[str, str]:
    """Create register data."""
    return {
        "name": DEFAULT_USERNAME,
        "login": DEFAULT_USERNAME,
        "email": EMAIL,
        "password": DEFAULT_USER_PASSWORD,
    }
