from apps.projects.models import Project, ProjectMember
from apps.users.models import User


def can_upload_project_asset(user: User, project: Project) -> bool:
    """
    Check can user create project asset.

    Only project members can upload assets.
    """
    return ProjectMember.objects.filter(
        project=project,
        user=user,
    ).exists()
