import abc


class ICleanupMediaFilesService(abc.ABC):
    """Cleanup media files service interface."""

    @abc.abstractmethod
    def cleanup_media_files(self) -> None:
        """Cleanup media files."""
