from constance import config
from constance.test import override_config


def test_empty_value(tariff):
    """Test empty value."""
    assert config.DEFAULT_TARIFF is None


def test_set_value(tariff):
    """Test getting value."""
    with override_config(DEFAULT_TARIFF=tariff):
        assert config.DEFAULT_TARIFF == tariff
