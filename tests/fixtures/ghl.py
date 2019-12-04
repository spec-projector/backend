# -*- coding: utf-8 -*-

import pytest
from graphene_django.rest_framework.tests.test_mutation import mock_info
from graphql import ResolveInfo

from gql import schema
from tests.helpers.ghl_client import GraphQLClient


@pytest.fixture(scope='session')
def ghl_queries():
    return schema.get_query_type()


@pytest.fixture(scope='session')
def ghl_mutations():
    return schema.get_mutation_type()


@pytest.fixture()  # type: ignore
def ghl_client() -> GraphQLClient:
    return GraphQLClient()


@pytest.fixture()  # type: ignore
def ghl_auth_mock_info(user, rf) -> ResolveInfo:
    rf.set_user(user)
    request = rf.get('/graphql/')

    info = mock_info()
    info.context = request

    return info


@pytest.fixture()  # type: ignore
def ghl_mock_info(user, rf) -> ResolveInfo:
    request = rf.get('/graphql/')

    info = mock_info()
    info.context = request

    return info
