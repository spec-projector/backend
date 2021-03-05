from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError


class BaseChangePasswordError(BaseInfrastructureError):
    """Base registration error."""


class PasswordNotSetError(BaseChangePasswordError):
    """Password not set error."""

    code = "password_not_set"
    message = _("MSG__PASSWORD_NOT_SET")
