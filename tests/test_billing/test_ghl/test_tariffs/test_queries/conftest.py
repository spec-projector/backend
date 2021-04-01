import pytest


@pytest.fixture(scope="session")
def all_tariffs_query(ghl_queries):
    """Provides all tariffs graphql query."""
    return ghl_queries.fields["allTariffs"].resolver
