import pytest

from tests.test_billing.factories.tariff import TariffFactory


@pytest.fixture()
def tariffs(db):
    """Create tariff."""
    return TariffFactory.create_batch(3)


def test_query(ghl_client, ghl_raw, tariffs):
    """Test getting all users raw query."""
    response = ghl_client.execute(ghl_raw("all_tariffs"))

    assert "errors" not in response
    tariffs_response = response["data"]["allTariffs"]
    assert tariffs_response["count"] == len(tariffs)


def test_success(ghl_mock_info, all_tariffs_query, tariffs):
    """Test success all tariffs retrieving."""
    response = all_tariffs_query(root=None, info=ghl_mock_info)

    assert response.length == len(tariffs)
    assert set(response.iterable) == set(tariffs)
