import injector

from apps.projects.logic.services.project_asset import (
    ProjectAssetPermissionsService,
)


class ProjectLogicServicesModule(injector.Module):
    """Setup di for project services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(ProjectAssetPermissionsService)
