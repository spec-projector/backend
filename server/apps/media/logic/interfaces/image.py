import abc
from typing import Optional

from apps.media.models import Image


class IImageService(abc.ABC):
    """Image service."""

    @abc.abstractmethod
    def upload_image_from_url(self, inbound_url: str) -> Optional[Image]:
        """Upload image from any url."""
