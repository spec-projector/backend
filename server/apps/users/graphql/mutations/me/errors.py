from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError


class BaseUploadAvatarError(BaseInfrastructureError):
    """Base upload avatar error."""


class UserNotExistsError(BaseUploadAvatarError):
    """User not exists error."""

    code = "user_not_exists"
    message = _("MSG__USER_NOT_EXISTS")
