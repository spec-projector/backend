from django.core import validators
from django.utils.translation import gettext_lazy as _


class LoginValidator(validators.RegexValidator):
    """Login validator."""

    message = _("MSG__LOGIN_ENTER_VALID_VALUE")

    def __init__(self, *args, **kwargs):
        """Initialize."""
        kwargs["regex"] = r"^[a-z0-9\.\_\-]{6,15}$"
        super().__init__(*args, **kwargs)
