# -*- coding: utf-8 -*-

import httpretty
import pytest

from tests.helpers.gitlab_client import GitlabMock


@pytest.fixture()
def gl_mocker():
    httpretty.enable(allow_net_connect=False)

    yield GitlabMock()

    httpretty.disable()
