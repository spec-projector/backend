import abc

from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError


class ResetPasswordError(BaseInfrastructureError, metaclass=abc.ABCMeta):
    """Base class for reset password errors."""


class EmailNotExistsError(ResetPasswordError):
    """Wrong credentials error."""

    code = "email_not_exists"
    message = _("MSG__EMAIL_NOT_EXISTS")


class CodeValidationError(ResetPasswordError):
    """Code validation error."""

    code = "code_not_valid"
    message = _("MSG__CODE_NOT_VALID")
