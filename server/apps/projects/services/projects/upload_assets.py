import hashlib

from django.db import models


def assets_upload_to(instance: models.Model, filename: str) -> str:
    """Generate folder for uploads."""
    hash_result = hashlib.md5(str(instance.pk).encode())  # noqa: S303
    return "projects/{0}/{1}".format(hash_result.hexdigest(), filename)
