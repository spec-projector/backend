from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone
from pytest import raises
from rest_framework.exceptions import AuthenticationFailed

from apps.core.graphql.security.authentication import TokenAuthentication
from apps.users.services.token import create_user_token


@pytest.fixture()
def token_auth():
    return TokenAuthentication()


def test_fail(rf, token_auth):
    assert token_auth.authenticate(rf.get('/')) is None


def test_success(user, rf, token_auth):
    rf.set_user(user)

    assert token_auth.authenticate(rf.get('/')) is not None


def test_expired_token(user, rf, token_auth):
    token = create_user_token(user)
    token.created = timezone.now() - timedelta(
        minutes=settings.TOKEN_EXPIRE_PERIOD + 60
    )
    token.save()

    rf.set_user(user, token)

    with raises(AuthenticationFailed) as error:
        token_auth.authenticate(rf.get('/'))

    assert str(error.value.detail) == 'Token has expired'


def test_invalid_token(user, rf, token_auth):
    token = create_user_token(user)
    token.key += '123456'

    rf.set_user(user, token)

    with raises(AuthenticationFailed) as error:
        token_auth.authenticate(rf.get('/'))

    assert str(error.value.detail) == 'Invalid token.'
