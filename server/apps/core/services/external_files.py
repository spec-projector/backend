from tempfile import TemporaryFile

import requests
from django.core.files import File
from django.db.models.fields.files import FieldFile

from apps.core.logic.interfaces.external_files import IExternalFilesService

CHUNK_SIZE = 4096


class ExternalFilesService(IExternalFilesService):
    """Service for download external files."""

    def download_to_field(
        self,
        field: FieldFile,
        image_url: str,
        title: str,
    ) -> None:
        """Download file from url to field."""
        with TemporaryFile() as tmp_file:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()

            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                tmp_file.write(chunk)

            tmp_file.seek(0)
            field.save("{0}.png".format(title), File(tmp_file))
