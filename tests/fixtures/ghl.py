import pytest
from graphene_django.rest_framework.tests.test_mutation import mock_info
from graphql import ResolveInfo

from gql import schema
from tests.helpers.ghl_client import GraphQLClient


@pytest.fixture(scope="session")
def ghl_queries():
    """Provides graphql queries."""
    return schema.get_query_type()


@pytest.fixture(scope="session")
def ghl_mutations():
    """Provides graphql mutations."""
    return schema.get_mutation_type()


@pytest.fixture()
def ghl_client() -> GraphQLClient:
    """Provides graphql client."""
    return GraphQLClient()


@pytest.fixture()
def ghl_auth_mock_info(user, rf) -> ResolveInfo:
    """Provides graphql auth mock info."""
    rf.set_user(user)
    request = rf.get("/graphql/")

    resolve_info = mock_info()
    resolve_info.context = request

    return resolve_info


@pytest.fixture()
def ghl_mock_info(user, rf) -> ResolveInfo:
    """Provides graphql mock info."""
    request = rf.get("/graphql/")

    resolve_info = mock_info()
    resolve_info.context = request

    return resolve_info
