import pytest

from apps.billing.models import Tariff
from tests.test_billing.factories.tariff import TariffFactory


@pytest.fixture()
def tariff(db):
    """Create tariff."""
    return TariffFactory.create()


def test_query(ghl_client, ghl_raw, tariff):
    """Test getting tariff raw query."""
    response = ghl_client.execute(
        ghl_raw("tariff"),
        variable_values={"id": tariff.pk},
    )

    assert "errors" not in response
    assert response["data"]["tariff"]["id"] == str(tariff.id)


def test_success(ghl_mock_info, tariff_query, tariff):
    """Test success tariff retrieving."""
    response = tariff_query(root=None, info=ghl_mock_info, id=tariff.pk)

    assert response == tariff


def test_retrieve_not_exists(ghl_mock_info, tariff_query, tariff):
    """Test retrieve not exists."""
    tariff_pk = tariff.pk

    Tariff.objects.filter(pk=tariff_pk).delete()
    response = tariff_query(root=None, info=ghl_mock_info, id=tariff_pk)

    assert response is None
