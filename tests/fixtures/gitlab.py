import httpretty
import pytest
from django.conf import settings
from graphene_django.rest_framework.tests.test_mutation import mock_info
from graphql import ResolveInfo
from social_core.backends.gitlab import GitLabOAuth2

from tests.helpers.httpretty_client import HttprettyMock


class GitlabMock(HttprettyMock):
    """Gitlab api mocker."""

    base_api_url = "{0}/api/v4".format(settings.GITLAB_HOST)


@pytest.fixture()
def gl_mocker():
    """Provides gitlab api mocker."""
    httpretty.enable(allow_net_connect=False)

    yield GitlabMock()

    httpretty.disable()


@pytest.fixture()
def gl_token_request_info(rf) -> ResolveInfo:
    """Provides gitlab token request info."""
    request = rf.get(GitLabOAuth2.AUTHORIZATION_URL)
    setattr(request, "session", {"gitlab_state": "gitlab_state"})  # noqa: B010

    resolve_info = mock_info()
    resolve_info.context = request

    return resolve_info
