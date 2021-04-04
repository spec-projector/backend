from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class CloudPaymentsWebhookView(View):
    """Cloud payments webhook view."""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """Dispatch."""
        return super().dispatch(*args, **kwargs)

    def post(self, request) -> HttpResponse:
        """Request handler."""
        return HttpResponse()
