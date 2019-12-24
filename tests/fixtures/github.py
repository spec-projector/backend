# -*- coding: utf-8 -*-

import httpretty
import pytest
from django.conf import settings

from tests.helpers.httpretty_client import HttprettyMock


class GithubMock(HttprettyMock):
    base_api_url = settings.GITHUB_HOST


@pytest.fixture()
def gh_mocker():
    httpretty.enable(allow_net_connect=False)

    yield GithubMock()

    httpretty.disable()
