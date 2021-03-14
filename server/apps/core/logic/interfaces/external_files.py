import abc

from django.db.models.fields.files import FieldFile


class IExternalFilesService(abc.ABC):
    """Service for download external files."""

    @abc.abstractmethod
    def download_to_field(
        self,
        field: FieldFile,
        image_url: str,
        title: str,
    ) -> None:
        """Download file from url to field."""
