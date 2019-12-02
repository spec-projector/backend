# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def user_resolver(ghl_queries):
    return ghl_queries.fields['user'].resolver
