from pytest import raises
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import Token
from apps.users.services.auth import login_user
from tests.conftest import DEFAULT_USER_PASSWORD


def test_success(user):
    assert not Token.objects.exists()

    token = login_user(user.login, DEFAULT_USER_PASSWORD, None)

    assert token is not None
    assert Token.objects.exists()


def test_not_active(user):
    user.is_active = False
    user.save()

    with raises(AuthenticationFailed):
        login_user(user.login, DEFAULT_USER_PASSWORD, None)


def test_wrong_password(user):
    with raises(AuthenticationFailed):
        login_user(
            user.login,
            'wrong{0}'.format(DEFAULT_USER_PASSWORD),
            None,
        )


def test_empty_password(user):
    with raises(AuthenticationFailed):
        login_user(user.login, '', None)


def test_invalid_login(user):
    with raises(AuthenticationFailed):
        login_user(
            'wrong{0}'.format(user.login),
            DEFAULT_USER_PASSWORD,
            None,
        )


def test_empty_login(user):
    with raises(AuthenticationFailed):
        login_user('', DEFAULT_USER_PASSWORD, None)


def test_multitokens(user):
    assert not Token.objects.exists()

    login_user(user.login, DEFAULT_USER_PASSWORD, None)

    assert Token.objects.filter(user=user).count() == 1

    login_user(user.login, DEFAULT_USER_PASSWORD, None)

    assert Token.objects.filter(user=user).count() == 2
