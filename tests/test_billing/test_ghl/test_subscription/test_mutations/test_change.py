from apps.billing.models import ChangeSubscriptionRequest
from tests.test_billing.factories import TariffFactory


def test_query(user, ghl_client, ghl_raw):
    """Test raw query success."""
    tariff = TariffFactory.create()

    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("change"),
        variable_values={
            "input": {
                "hash": "12345",
                "tariff": tariff.pk,
            },
        },
    )

    assert "errors" not in response
    dto = response["data"]["changeSubscription"]["request"]
    assert dto is not None

    assert ChangeSubscriptionRequest.objects.filter(
        id=dto["id"],
        user=user,
        is_active=True,
    ).exists()
