import httpretty
import pytest
from django.conf import settings

from tests.helpers.httpretty_client import HttprettyMock


class GithubMock(HttprettyMock):
    """GitHub api mocker."""

    base_api_url = settings.GITHUB_HOST


@pytest.fixture()
def gh_mocker():
    """Providers GitHub api mocker."""
    httpretty.enable(allow_net_connect=False)

    yield GithubMock()

    httpretty.disable()
