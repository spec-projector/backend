import os

from django.db import models

from apps.projects.models import ProjectAsset


def cleanup_project_assets() -> None:
    """
    Delete projectAsset's files with a null project.

    After files are deleted - delete objects from DB.
    """
    _cleanup_files()
    _cleanup_project_assets()


def _cleanup_files() -> None:
    """Cleanup files."""
    assets = _get_project_assets_for_cleanup()
    for asset in assets.filter(file__isnull=False):
        file_path = asset.file.path
        _remove_file(file_path)
        if not os.path.exists(file_path):
            asset.file = None
            asset.save()


def _cleanup_project_assets() -> None:
    """Cleanup project assets without files."""
    assets = _get_project_assets_for_cleanup()
    assets.filter(file__in=["", None]).delete()


def _get_project_assets_for_cleanup() -> models.QuerySet:
    """Get project assets for delete."""
    return ProjectAsset.objects.filter(project__isnull=True)


def _remove_file(file_path: str) -> None:
    """Remove file if exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
