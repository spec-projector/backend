# -*- coding: utf-8 -*-

from pytest import raises
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import Token
from tests.fixtures.users import DEFAULT_USER_PASSWORD, DEFAULT_USERNAME

GHL_QUERY_LOGIN = """
mutation {{
    login(input: {{ username: "{login}", password: "{password}" }} ) {{
        token {{
          key
        }}
    }}
}}
"""


def test_query(user, ghl_client):
    """Test login raw query."""
    assert not Token.objects.filter(user=user).exists()

    result = ghl_client.execute(GHL_QUERY_LOGIN.format(
        login=DEFAULT_USERNAME,
        password=DEFAULT_USER_PASSWORD,
    ))

    assert 'errors' not in result

    token = Token.objects.filter(user=user).first()
    assert token is not None
    assert result['data']['login']['token']['key'] == token.key


def test_success(user, ghl_mock_info, login_mutation):
    """Test success login."""
    assert not Token.objects.filter(user=user).exists()

    result = login_mutation(
        root=None,
        info=ghl_mock_info,
        input={
            'username': DEFAULT_USERNAME,
            'password': DEFAULT_USER_PASSWORD,
        },
    )

    assert Token.objects.filter(pk=result.token.pk, user=user).exists()


def test_wrong_username(user, ghl_mock_info, login_mutation):
    """Test wrong username case."""
    assert not Token.objects.filter(user=user).exists()

    with raises(AuthenticationFailed):
        login_mutation(
            None,
            ghl_mock_info,
            input={
                'username': 'wrong{0}'.format(DEFAULT_USERNAME),
                'password': DEFAULT_USER_PASSWORD,
            },
        )

    assert not Token.objects.filter(user=user).exists()


def test_wrong_password(user, ghl_mock_info, login_mutation):
    """Test wrong password case."""
    assert not Token.objects.filter(user=user).exists()

    with raises(AuthenticationFailed):
        login_mutation(
            None,
            ghl_mock_info,
            input={
                'username': DEFAULT_USERNAME,
                'password': 'wrong{0}'.format(DEFAULT_USER_PASSWORD),
            },
        )

    assert not Token.objects.filter(user=user).exists()
