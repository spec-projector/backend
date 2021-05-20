from django.db import models

from apps.projects.models import ProjectAsset


class ProjectAssetCleanupService:
    """Removes obsolete project assets."""

    def cleanup(self) -> None:
        """Delete projectAsset's with a null project."""
        self._cleanup_project_assets()

    def _cleanup_project_assets(self) -> None:
        """Cleanup project assets without files."""
        assets = self._get_project_assets_for_cleanup()
        assets.filter(file__isnull=True).delete()

    def _get_project_assets_for_cleanup(self) -> models.QuerySet:
        """Get project assets for delete."""
        return ProjectAsset.objects.filter(project__isnull=True)
