from apps.projects.models import Project, ProjectMember
from apps.users.models import User


def can_upload_project_asset(user: User, project: Project) -> bool:
    """
    Check can user create project asset.

    Only project owner or project members can upload assets.
    """
    project_member = ProjectMember.objects.filter(
        project=project,
        user=user,
    )

    return project.owner == user or project_member.exists()
