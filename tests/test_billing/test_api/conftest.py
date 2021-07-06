import pytest

from tests.test_billing.factories import TariffFactory


@pytest.fixture()
def tariff(db):
    """Create tariff."""
    return TariffFactory.create()
