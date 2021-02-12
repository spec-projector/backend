from apps.core.services.figma import (
    IFigmaService,
    IFigmaServiceFactory,
    ImageParams,
)


class StubFigmaService(IFigmaService):
    """Mocked figma service."""

    def get_image_params(self, inbound_url) -> ImageParams:
        """Get mock image params."""
        return ImageParams("key", "title", "id")

    def get_image_url(self, inbound_url: str) -> str:
        """Get direct url for image."""
        return "https://test.com/image.png"


class StubFigmaFactoryService(IFigmaServiceFactory):
    """Mocked figma factory."""

    def create(self, token: str) -> IFigmaService:
        """Create mocked figma service."""
        return StubFigmaService(token)
