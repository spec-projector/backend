import hashlib

from apps.projects.models import ProjectAsset


def assets_upload_to(project_asset: ProjectAsset, filename: str) -> str:
    """Generate folder for uploads."""
    project_hash = hashlib.md5(  # noqa: S303
        str(project_asset.project.pk).encode(),
    ).hexdigest()
    return "projects/{0}/{1}".format(project_hash, filename)
