from typing import Dict

from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from apps.users.models import User
from tests.fixtures.users import DEFAULT_USER_PASSWORD

EMAIL = "new_user@mail.net"


def test_query(db, default_tariff_config, default_tariff, ghl_client, ghl_raw):
    """Test register raw query."""
    assert not User.objects.filter(email=EMAIL).exists()

    register_data = _get_register_data()
    register_data["firstName"] = register_data.pop("first_name")
    register_data["lastName"] = register_data.pop("last_name")

    response = ghl_client.execute(
        ghl_raw("register"),
        variable_values={
            "input": register_data,
        },
    )

    assert "errors" not in response

    user = User.objects.get(email=EMAIL)

    assert Subscription.objects.filter(
        user=user,
        status=SubscriptionStatus.ACTIVE,
        tariff=default_tariff,
    )


def _get_register_data() -> Dict[str, str]:
    """Create register data."""
    return {
        "email": EMAIL,
        "password": DEFAULT_USER_PASSWORD,
        "first_name": "first name",
        "last_name": "last name",
    }
