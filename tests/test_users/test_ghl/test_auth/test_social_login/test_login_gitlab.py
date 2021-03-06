import pytest
from django.conf import settings
from social_core.backends.gitlab import GitLabOAuth2

from apps.users.logic.interfaces.social_login import SystemBackend


@pytest.fixture(scope="module", autouse=True)
def _gitlab_login() -> None:
    """Forces django to use gitlab settings."""
    settings.SOCIAL_AUTH_GITLAB_REDIRECT_URI = "redirect_uri"
    settings.SOCIAL_AUTH_GITLAB_KEY = "test_gitlab_key"
    settings.SOCIAL_AUTH_GITLAB_SECRET = "test_gitlab_secret"


def test_query(user, ghl_client, ghl_raw):
    """Test raw query."""
    context = {
        "session": {},
        "GET": {},
        "POST": {},
        "build_absolute_uri": lambda mock: mock,
        "method": "",
    }

    response = ghl_client.execute(
        ghl_raw("social_login"),
        extra_context=context,
        variable_values={
            "system": SystemBackend.GITLAB.name,
        },
    )

    assert "errors" not in response
    redirect_url = response["data"]["socialLogin"]["redirectUrl"]

    client = "client_id={0}".format(settings.SOCIAL_AUTH_GITLAB_KEY)
    redirect = "redirect_uri={0}".format(
        settings.SOCIAL_AUTH_GITLAB_REDIRECT_URI,
    )

    assert redirect_url.startswith(GitLabOAuth2.AUTHORIZATION_URL)
    assert client in redirect_url
    assert redirect in redirect_url
