from django.db import models
from rest_framework.request import Request


def get_absolute_path(
    file_field: models.FileField,
    request: Request,
) -> str:
    """Generate absolute file path."""
    if file_field:
        return request.build_absolute_uri(file_field.url)
    return file_field
