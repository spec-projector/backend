# -*- coding: utf-8 -*-

import pytest
from django.conf import settings
from social_core.backends.gitlab import GitLabOAuth2

from apps.users.models import Token

GHL_QUERY_LOGIN_GITLAB = """
mutation {
  loginGitlab {
    redirectUrl
  }
}
"""


@pytest.fixture(scope="module", autouse=True)
def _gitlab_login() -> None:
    """Forces django to use gitlab settings."""
    settings.SOCIAL_AUTH_GITLAB_REDIRECT_URI = "redirect_uri"
    settings.SOCIAL_AUTH_GITLAB_KEY = "test_gitlab_key"
    settings.SOCIAL_AUTH_GITLAB_SECRET = "test_gitlab_secret"


def test_query(user, ghl_client):
    """Test raw query."""
    context = {
        "session": {},
        "GET": {},
        "POST": {},
        "build_absolute_uri": lambda mock: mock,
        "method": "",
    }

    response = ghl_client.execute(
        GHL_QUERY_LOGIN_GITLAB,
        extra_context=context,
    )

    assert "errors" not in response

    redirect_url = response["data"]["loginGitlab"]["redirectUrl"]

    client = "client_id={0}".format(settings.SOCIAL_AUTH_GITLAB_KEY)
    redirect = "redirect_uri={0}".format(
        settings.SOCIAL_AUTH_GITLAB_REDIRECT_URI,
    )

    assert redirect_url.startswith(GitLabOAuth2.AUTHORIZATION_URL)
    assert client in redirect_url
    assert redirect in redirect_url


def test_complete_login(
    user,
    gl_mocker,
    complete_gl_auth_mutation,
    gl_token_request_info,
):
    """Test complete login."""
    gl_mocker.register_get("/user", {
        "id": user.pk,
        "username": user.login,
        "email": user.email,
    })

    gl_mocker.base_api_url = GitLabOAuth2.ACCESS_TOKEN_URL
    gl_mocker.register_post("", {
        "access_token": "access_token",
        "token_type": "bearer",
        "expires_in": 7200,
        "refresh_token": "refresh_token",
    })

    response = complete_gl_auth_mutation(
        root=None,
        info=gl_token_request_info,
        code="test_code",
        state=gl_token_request_info.context.session["gitlab_state"],
    )

    assert not response.errors
    assert Token.objects.filter(pk=response.token.pk, user=user).exists()


def test_not_login(
    user,
    gl_mocker,
    complete_gl_auth_mutation,
    gl_token_request_info,
):
    """Test not login user."""
    gl_mocker.register_get("/user", {
        "id": user.pk,
        "username": "test_user",
        "email": user.email,
    })

    gl_mocker.base_api_url = GitLabOAuth2.ACCESS_TOKEN_URL
    gl_mocker.register_post("", {
        "access_token": "access_token",
        "token_type": "bearer",
        "expires_in": 7200,
        "refresh_token": "refresh_token",
    })

    response = complete_gl_auth_mutation(
        root=None,
        info=gl_token_request_info,
        code="test_code",
        state=gl_token_request_info.context.session["gitlab_state"],
    )

    assert response.errors
    assert not response.token
