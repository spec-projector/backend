import logging
from http import HTTPStatus

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.billing.logic.use_cases.subscription import payment_webhook
from apps.core import injector
from apps.core.logic.errors import BaseApplicationError
from apps.core.services.errors import BaseInfrastructureError

logger = logging.getLogger(__name__)


class CloudPaymentsWebhookView(View):
    """Cloud payments webhook view."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """Dispatch."""
        return super().dispatch(*args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Request handler."""
        logging.info("CloudPayment webhook was triggered")

        command = injector.get(payment_webhook.UseCase)
        raw_body = request.body

        try:
            command.execute(
                payment_webhook.InputDto(
                    payment_data=dict(request.POST.items()),
                    payment_meta=dict(request.headers.items()),
                    raw_body=raw_body,
                ),
            )
        except (BaseInfrastructureError, BaseApplicationError):
            return HttpResponse(status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({"code": 0})
