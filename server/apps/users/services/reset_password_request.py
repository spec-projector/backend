from django.utils import timezone

from apps.users.logic.interfaces.reset_password_request import (
    IResetPasswordRequestService,
)
from apps.users.models import ResetPasswordRequest, User


class ResetPasswordRequestService(IResetPasswordRequestService):
    """Service for reset password request."""

    def create_reset_password_request(
        self,
        user: User,
    ) -> ResetPasswordRequest:
        """Create reset password request for user."""
        return ResetPasswordRequest.objects.create(user=user)

    def code_valid(self, user: User, code: str) -> bool:
        """Validate code."""
        return ResetPasswordRequest.objects.filter(
            user=user,
            code=code,
            expired_at__gt=timezone.now(),
        ).exists()
