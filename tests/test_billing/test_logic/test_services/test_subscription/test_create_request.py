import pytest

from apps.billing.logic.services.subscription import SameTariffChangeError
from apps.billing.models import ChangeSubscriptionRequest
from tests.test_billing.factories import SubscriptionFactory, TariffFactory


def test_new(user, subscription_service):
    """Test new request."""
    assert not ChangeSubscriptionRequest.objects.exists()
    tariff = TariffFactory.create()
    request_hash = "124"
    request = subscription_service.create_change_subscription_request(
        user,
        tariff,
        request_hash,
    )

    assert request.tariff == tariff
    assert request.hash == request_hash


def test_same_tariff(user, subscription_service):
    """Test same tariff."""
    assert not ChangeSubscriptionRequest.objects.exists()

    tariff = TariffFactory.create()

    SubscriptionFactory.create(user=user, tariff=tariff)

    with pytest.raises(SameTariffChangeError):
        subscription_service.create_change_subscription_request(
            user,
            tariff,
            "123",
        )
