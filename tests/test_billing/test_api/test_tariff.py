from http import HTTPStatus

from apps.core.admin.api.autocomplete_view import AutocompleteSerializer
from tests.test_billing.factories import TariffFactory

API_URL = "/admin/billing/tariff/autocomplete/"


def test_success(admin_user, tariff, admin_client):
    """Test success."""
    response = admin_client.get(API_URL)

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert (
        response_data["results"]
        == AutocompleteSerializer(instance=[tariff], many=True).data
    )


def test_not_is_active(admin_user, tariff, admin_client):
    """Test get empty data."""
    tariff.is_active = False
    tariff.save()
    response = admin_client.get(API_URL)

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert not response_data["results"]


def test_find(admin_user, tariff, admin_client):
    """Test find values."""
    response = admin_client.get(API_URL, {"term": tariff.pk})

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert (
        response_data["results"]
        == AutocompleteSerializer(instance=[tariff], many=True).data
    )


def test_not_find(admin_user, tariff, admin_client):
    """Test find values."""
    response = admin_client.get(API_URL, {"term": "xxxxxxx"})

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert not response_data["results"]


def test_paging(admin_user, tariff, admin_client):
    """Test find values."""
    TariffFactory.create_batch(20)
    response = admin_client.get(API_URL, {"page": "2"})

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert len(response_data["results"]) == 1
