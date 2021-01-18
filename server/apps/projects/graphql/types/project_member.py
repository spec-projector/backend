import graphene
from jnt_django_graphene_toolbox.fields import BitField
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.projects.models import ProjectMember
from apps.users.graphql.types import UserType


class ProjectMemberType(BaseModelObjectType):
    """Project member type."""

    class Meta:
        model = ProjectMember

    roles = BitField()
    user = graphene.Field(UserType)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
