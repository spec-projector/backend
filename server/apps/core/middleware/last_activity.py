from django.utils import timezone


class LastActivityMiddleware:
    """Last activity middleware."""

    def __init__(self, get_response):
        """Init middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call middleware."""
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save()

        return self.get_response(request)
