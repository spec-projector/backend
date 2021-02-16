import graphene

from apps.projects.graphql.resolvers.issue import resolve_issue
from apps.projects.graphql.types import IssueType
from apps.projects.services.issues.meta import System


class IssueInput(graphene.InputObjectType):
    """Input for get issue."""

    project = graphene.ID(required=True)
    url = graphene.String(required=True)
    system = graphene.Enum.from_enum(System)(required=True)


class IssuesQueries(graphene.ObjectType):
    """Issue queries."""

    issue = graphene.Field(
        IssueType,
        resolver=resolve_issue,
        input=graphene.Argument(IssueInput, required=True),
    )
