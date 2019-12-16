# -*- coding: utf-8 -*-

import httpretty
import pytest
from django.conf import settings

from tests.helpers.httppretty_client import HttprettyMock


class GitlabMock(HttprettyMock):
    base_api_url = '{0}/api/v4'.format(settings.GITLAB_HOST)


@pytest.fixture()
def gl_mocker():
    httpretty.enable(allow_net_connect=False)

    yield GitlabMock()

    httpretty.disable()
