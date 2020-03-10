# -*- coding: utf-8 -*-

from datetime import timedelta

import pytest
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from apps.core.graphql.security.authentication import TokenAuthentication
from apps.users.models import Token, User
from apps.users.services.token import create_user_token


@pytest.fixture()
def auth() -> TokenAuthentication:
    """Provides token authentication."""
    return TokenAuthentication()


@pytest.fixture()
def user_token(user: User) -> Token:
    """Provides user token."""
    return create_user_token(user)


def set_http_auth_header(request: HttpRequest, token: Token) -> None:
    """Set auth header to request."""
    request.META.update(HTTP_AUTHORIZATION="Bearer {0}".format(token.key))


def test_fail(rf, auth):
    """Test auth failing."""
    assert auth.authenticate(rf.get("/")) is None


def test_success(rf, auth, user_token):
    """Test auth success."""
    request = rf.get("/")
    set_http_auth_header(request, user_token)

    assert auth.authenticate(request) is not None


def test_expired_token(rf, auth, user_token):
    """Test expired token."""
    user_token.created = timezone.now() - timedelta(
        minutes=settings.TOKEN_EXPIRE_PERIOD + 60,
    )
    user_token.save()

    request = rf.get("/")
    set_http_auth_header(request, user_token)

    with pytest.raises(AuthenticationFailed, match="Token has expired"):
        auth.authenticate(request)


def test_invalid_token(rf, auth, user_token):
    """Test invalid token."""
    user_token.key = "{0}123456".format(user_token.key)

    request = rf.get("/")
    set_http_auth_header(request, user_token)

    with pytest.raises(AuthenticationFailed, match="Invalid token."):
        auth.authenticate(request)
