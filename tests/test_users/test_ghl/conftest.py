# -*- coding: utf-8 -*-

import pytest


@pytest.fixture(scope='session')
def login_mutation(ghl_mutations):
    return ghl_mutations.fields['login'].resolver
