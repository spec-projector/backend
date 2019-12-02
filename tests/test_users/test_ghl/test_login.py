from pytest import raises
from rest_framework.exceptions import AuthenticationFailed

from apps.users.graphql.mutations.login import LoginMutation
from apps.users.models import Token
from tests.conftest import DEFAULT_USERNAME, DEFAULT_USER_PASSWORD

GHL_QUERY_LOGIN = """
mutation {{
    login(login: "{login}", password: "{password}") {{
        token {{
          key
        }}
    }}
}}
"""


def test_query(user, ghl_client):
    """Test login query."""
    assert not Token.objects.filter(user=user).exists()

    result = ghl_client.execute(GHL_QUERY_LOGIN.format(
        login=DEFAULT_USERNAME,
        password=DEFAULT_USER_PASSWORD,
    ))

    assert 'errors' not in result

    token = Token.objects.filter(user=user).first()
    assert token is not None
    assert result['data']['login']['token']['key'] == token.key


def test_success(user, ghl_mock_info):
    """Test success login."""
    assert not Token.objects.filter(user=user).exists()

    result = LoginMutation().mutate(
        None,
        ghl_mock_info,
        login=DEFAULT_USERNAME,
        password=DEFAULT_USER_PASSWORD,
    )

    assert Token.objects.filter(pk=result.token.pk, user=user).exists()


def test_fail(user, ghl_mock_info):
    """Test wrong login case."""

    assert not Token.objects.filter(user=user).exists()

    with raises(AuthenticationFailed):
        LoginMutation().mutate(
            None,
            ghl_mock_info,
            login='wrong{0}'.format(DEFAULT_USERNAME),
            password=DEFAULT_USER_PASSWORD,
        )

    assert not Token.objects.filter(user=user).exists()
