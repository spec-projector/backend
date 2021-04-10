import json
from http import HTTPStatus
from urllib import parse  # noqa: WPS347

import pytest

from tests.test_billing.factories import TariffFactory
from tests.test_users.factories.user import UserFactory


@pytest.fixture()
def cloud_payment(override_config):  # noqa: PT004
    """Cloud Payment config override."""
    with override_config(
        CLOUD_PAYMENT_PUBLIC_ID="123456",
        CLOUD_PAYMENT_API_SECRET="654321",
    ):
        yield


def test_success(db, client, subscription_service, cloud_payment):
    """Test positive."""
    user = UserFactory.create(pk=1, email="user@mail.com")
    tariff = TariffFactory.create(pk=1)
    custom_data = {
        "user": str(user.pk),
        "tariff": str(tariff.pk),
        "hash": "222222",
    }

    response = client.post(
        "/webhooks/cloud_payments",
        data=parse.urlencode(
            {
                "OperationType": "Payment",
                "Email": user.email,
                "SubscriptionId": "111111",
                "Status": "Authorized",
                "Data": json.dumps(custom_data),
            },
            doseq=True,
        ),
        content_type="application/x-www-form-urlencoded",
        HTTP_CONTENT_HMAC="+GnpyzU3P6AJvUvsZ7FiRECp/w9nvL8Ga80OtaEy+Lc=",
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"code": 0}

    subscription = subscription_service.get_user_subscription(user)
    assert subscription.tariff == tariff


def test_wrong_signature(user, client, subscription_service, cloud_payment):
    """Test bad signature."""
    tariff = TariffFactory.create()
    custom_data = {
        "user": str(user.pk),
        "tariff": str(tariff.pk),
        "hash": "222222",
    }

    response = client.post(
        "/webhooks/cloud_payments",
        data=parse.urlencode(
            {
                "OperationType": "Payment",
                "Email": user.email,
                "SubscriptionId": "111111",
                "Status": "Authorized",
                "Data": json.dumps(custom_data),
            },
            doseq=True,
        ),
        content_type="application/x-www-form-urlencoded",
        HTTP_CONTENT_HMAC="1111",
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
