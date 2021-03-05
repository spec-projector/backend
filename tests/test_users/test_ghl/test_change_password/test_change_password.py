from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from apps.core import injector
from apps.users.logic.interfaces import IAuthenticationService

NEW_PASSWORD = "new user password"  # noqa: S105


def test_query(user, ghl_client, ghl_raw):
    """Test change password raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("change_password"),
        variable_values={
            "input": {
                "password": NEW_PASSWORD,
            },
        },
    )

    assert "errors" not in response

    assert response["data"]["changePassword"]["ok"]
    _check_auth(user.login, NEW_PASSWORD)


def test_success(user, ghl_auth_mock_info, change_password_mutation):
    """Test success change password."""
    response = change_password_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={"password": NEW_PASSWORD},
    )

    assert response.ok
    _check_auth(user.login, NEW_PASSWORD)


def test_change_not_auth(user, ghl_mock_info, change_password_mutation):
    """Test not change password."""
    old_password = "old_password"  # noqa: S105

    user.set_password(old_password)
    user.save()

    response = change_password_mutation(
        root=None,
        info=ghl_mock_info,
        input={"password": NEW_PASSWORD},
    )

    assert isinstance(response, GraphQLPermissionDenied)
    _check_auth(user.login, old_password)


def _check_auth(username, password) -> None:
    """Check success auth with password."""
    auth = injector.get(IAuthenticationService)
    assert auth.auth(username, password)
