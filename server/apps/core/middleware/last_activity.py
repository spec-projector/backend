from apps.core.logic import commands
from apps.users.logic.commands.user import UpdateUserActivityCommand


class LastActivityMiddleware:
    """Last activity middleware."""

    def __init__(self, get_response):
        """Init middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Call middleware."""
        response = self.get_response(request)
        if request.user.is_authenticated:
            commands.execute_command(
                UpdateUserActivityCommand(request.user.pk),
            )

        return response
