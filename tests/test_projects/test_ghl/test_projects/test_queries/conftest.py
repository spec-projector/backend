# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope="session")
def project_query(ghl_queries):
    return ghl_queries.fields["project"].resolver


@pytest.fixture(scope="session")
def all_projects_query(ghl_queries):
    return ghl_queries.fields["allProjects"].resolver
