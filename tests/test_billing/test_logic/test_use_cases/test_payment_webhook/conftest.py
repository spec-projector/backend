import pytest

from apps.billing.logic.use_cases.subscription import payment_webhook
from apps.core import injector


@pytest.fixture()
def use_case():
    """Provide payment webhook usecase."""
    return injector.get(payment_webhook.UseCase)
