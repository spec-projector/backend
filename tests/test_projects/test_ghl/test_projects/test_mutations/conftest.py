# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def create_project_mutation(ghl_mutations):
    return ghl_mutations.fields['createProject'].resolver


@pytest.fixture(scope='session')
def delete_project_mutation(ghl_mutations):
    return ghl_mutations.fields['deleteProject'].resolver
