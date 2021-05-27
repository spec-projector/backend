import graphene
from jnt_django_graphene_toolbox.fields import BitField

from apps.projects.models.enums import ProjectMemberRole, ProjectPermission


class ProjectMeType(graphene.ObjectType):
    """Me project type."""

    role = graphene.Enum.from_enum(ProjectMemberRole)()
    permissions = BitField(ProjectPermission)
