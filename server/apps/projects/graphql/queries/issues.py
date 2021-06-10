import graphene
from graphql import ResolveInfo
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from apps.core.logic import queries
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
        **kwargs,
    ) -> retrieve.Issue:
        """Resolve issue."""
        if not info.context.user.is_authenticated:  # type: ignore
            raise GraphQLPermissionDenied()

        input_data = kwargs["input"]
        return queries.execute_query(
            retrieve.Query(
                project=input_data.project,
                url=input_data.url,
                system=IssuesManagementSystem(input_data.system),
            ),
        )
