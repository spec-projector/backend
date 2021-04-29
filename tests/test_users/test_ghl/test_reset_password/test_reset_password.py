import pytest

from apps.users.logic.commands.reset_password.errors import EmailNotExistsError
from apps.users.models import Token
from tests.test_users.factories.reset_password_request import (
    ResetPasswordRequestFactory,
)

NEW_PASSWORD = "new pass"  # noqa: S105


def test_query(user, ghl_client, ghl_raw):
    """Test login raw query."""
    reset_request = ResetPasswordRequestFactory.create(user=user)
    response = ghl_client.execute(
        ghl_raw("reset_password"),
        variable_values={
            "input": {
                "email": user.email,
                "code": reset_request.code,
                "password": NEW_PASSWORD,
            },
        },
    )

    assert "errors" not in response
    assert Token.objects.get(
        user=user,
        key=response["data"]["resetPassword"]["token"]["key"],
    )
    _check_auth(user)


def test_success(user, ghl_mock_info, reset_password_mutation):
    """Test success login."""
    reset_request = ResetPasswordRequestFactory.create(user=user)
    response = reset_password_mutation(
        root=None,
        info=ghl_mock_info,
        input={
            "email": user.email,
            "code": reset_request.code,
            "password": NEW_PASSWORD,
        },
    )

    assert Token.objects.filter(pk=response.token.pk, user=user).exists()
    _check_auth(user)


def test_wrong_email(user, ghl_mock_info, reset_password_mutation):
    """Test success login."""
    reset_request = ResetPasswordRequestFactory.create(user=user)
    with pytest.raises(EmailNotExistsError):
        reset_password_mutation(
            root=None,
            info=ghl_mock_info,
            input={
                "email": "wrong@email.bad",
                "code": reset_request.code,
                "password": NEW_PASSWORD,
            },
        )


def _check_auth(user) -> None:
    """Check auth by new password."""
    user.refresh_from_db()
    assert user.check_password(NEW_PASSWORD)
