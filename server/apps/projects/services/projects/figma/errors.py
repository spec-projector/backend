from django.utils.translation import gettext_lazy as _

from apps.core.errors import BaseError


class FigmaError(BaseError):
    """Main figma-exception."""


class IntegrationNotFoundFigmaError(FigmaError):
    """Figma integration not found."""

    code: str = "figma_integration_not_found"
    message = _("MSG__FIGMA_INTEGRATION_NOT_FOUND")


class InvalidUrlFigmaError(FigmaError):
    """Figma integration not found."""

    code: str = "figma_invalid_url"
    message = _("MSG__FIGMA_NOT_VALID_URL")


class ApiFigmaError(FigmaError):
    """Figma api exception."""

    code: str = "figma_api_error"

    def __init__(self, message) -> None:
        """Initialize."""
        self.message = message
        super().__init__()
