import os

from django.db import models

from apps.projects.models import ProjectAsset


class ProjectAssetCleanupService:
    """Removes obsolete project assets."""

    def cleanup(self) -> None:
        """
        Delete projectAsset's files with a null project.

        After files are deleted - delete objects from DB.
        """
        self._cleanup_files()
        self._cleanup_project_assets()

    def _cleanup_files(self) -> None:
        """Cleanup files."""
        assets = self._get_project_assets_for_cleanup()
        for asset in assets.filter(file__isnull=False):
            file_path = asset.file.path
            self._remove_file(file_path)
            if not os.path.exists(file_path):
                asset.file = None
                asset.save()

    def _cleanup_project_assets(self) -> None:
        """Cleanup project assets without files."""
        assets = self._get_project_assets_for_cleanup()
        assets.filter(file__in=["", None]).delete()

    def _get_project_assets_for_cleanup(self) -> models.QuerySet:
        """Get project assets for delete."""
        return ProjectAsset.objects.filter(project__isnull=True)

    def _remove_file(self, file_path: str) -> None:
        """Remove file if exists."""
        if os.path.exists(file_path):
            os.remove(file_path)
