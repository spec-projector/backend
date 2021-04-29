from typing import Generator

import pytest

from apps.billing.models import Tariff
from tests.test_billing.factories import TariffFactory


@pytest.fixture()
def default_tariff(override_config) -> Tariff:
    """Create default tariff."""
    return TariffFactory.create()


@pytest.fixture()
def default_tariff_config(  # noqa: PT004
    override_config,
    default_tariff,
) -> Generator[None, None, None]:
    """Add default tariff to config."""
    with override_config(
        DEFAULT_TARIFF=default_tariff,
    ):
        yield


@pytest.fixture()
def command_data():
    """Create register command."""
    return {
        "first_name": "new user",
        "email": "new_user@mail.net",
        "last_name": "newuser",
        "password": "123456",
    }
