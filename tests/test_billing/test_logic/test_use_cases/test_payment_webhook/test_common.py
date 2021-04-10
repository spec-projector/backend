import json

from apps.billing.logic.use_cases.subscription import payment_webhook
from apps.billing.models import ChangeSubscriptionRequest, Subscription
from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import TariffFactory


def test_request_no_exists(use_case, user):
    """Test if request is not created."""
    tariff = TariffFactory.create()
    use_case.execute(
        payment_webhook.InputDto(
            payment_data={
                "OperationType": "Payment",
                "SubscriptionId": "1111",
                "Email": user.email,
                "Status": "Authorized",
                "Data": json.dumps(
                    {
                        "user": str(user.pk),
                        "tariff": str(tariff.pk),
                        "hash": "222222",
                    },
                ),
            },
            payment_meta={},
            raw_body=b"",
        ),
    )

    assert Subscription.objects.count() == 1
    subscription = Subscription.objects.filter(
        user=user,
        tariff=tariff,
        status=SubscriptionStatus.ACTIVE,
    ).first()
    assert subscription is not None

    assert ChangeSubscriptionRequest.objects.count() == 1
    request = ChangeSubscriptionRequest.objects.filter(
        user=user,
        is_active=False,
        hash="222222",
        tariff=tariff,
        to_subscription=subscription,
        from_subscription=None,
    ).first()
    assert request is not None


def test_request_exists(use_case, user):
    """Test if request is created."""
    tariff = TariffFactory.create()
    request = ChangeSubscriptionRequest.objects.create(
        user=user,
        hash="222222",
        tariff=tariff,
    )

    use_case.execute(
        payment_webhook.InputDto(
            payment_data={
                "OperationType": "Payment",
                "SubscriptionId": "1111",
                "Email": user.email,
                "Status": "Authorized",
                "Data": json.dumps(
                    {
                        "user": str(user.pk),
                        "tariff": str(tariff.pk),
                        "hash": "222222",
                    },
                ),
            },
            payment_meta={},
            raw_body=b"",
        ),
    )

    assert Subscription.objects.count() == 1
    subscription = Subscription.objects.filter(
        user=user,
        tariff=tariff,
        status=SubscriptionStatus.ACTIVE,
    ).first()
    assert subscription is not None

    assert ChangeSubscriptionRequest.objects.count() == 1
    request.refresh_from_db()
    assert not request.is_active
