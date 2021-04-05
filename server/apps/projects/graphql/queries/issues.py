import graphene
from graphql import ResolveInfo

from apps.core import injector
from apps.projects.graphql.types import IssueType
from apps.projects.logic.interfaces.issues import IssuesManagementSystem
from apps.projects.logic.queries.issue import retrieve


class IssueInput(graphene.InputObjectType):
    """Input for get issue."""

    project = graphene.ID(required=True)
    url = graphene.String(required=True)
    system = graphene.Enum.from_enum(IssuesManagementSystem)(required=True)


class IssuesQueries(graphene.ObjectType):
    """Issue queries."""

    issue = graphene.Field(
        IssueType,
        input=graphene.Argument(IssueInput, required=True),
    )

    def resolve_issue(
        self,
        info: ResolveInfo,  # noqa: WPS110
        input_dto,
    ) -> retrieve.Issue:
        """Resolve issue."""
        return injector.get(retrieve.Query).execute(
            retrieve.InputDto(
                project=input_dto.project,
                url=input_dto.url,
                system=IssuesManagementSystem(input_dto.system),
            ),
        )
