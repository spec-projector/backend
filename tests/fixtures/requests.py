# -*- coding: utf-8 -*-

import pytest

from tests.helpers.request_factory import RequestFactory


@pytest.fixture()
def rf() -> RequestFactory:
    return RequestFactory()
