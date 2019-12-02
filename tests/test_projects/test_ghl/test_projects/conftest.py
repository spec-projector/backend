# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def project_resolver(ghl_queries):
    return ghl_queries.fields['project'].resolver


@pytest.fixture(scope='session')
def all_projects_resolver(ghl_queries):
    return ghl_queries.fields['allProjects'].resolver
