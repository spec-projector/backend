import graphene
from graphene_django.debug import DjangoDebug
from jnt_django_graphene_toolbox import scheme

from apps.billing.graphql.mutations import BillingMutations
from apps.billing.graphql.queries import BillingQueries
from apps.core.graphql.views import ApiGraphQLView, PlaygroundGraphQLView
from apps.media.graphql.mutations import MediaMutations
from apps.projects.graphql.mutations import ProjectsMutations
from apps.projects.graphql.queries import ProjectsQueries
from apps.users.graphql.mutations import UsersMutations
from apps.users.graphql.queries import UsersQueries


class Query(  # noqa: WPS215
    ProjectsQueries,
    UsersQueries,
    BillingQueries,
    graphene.ObjectType,
):
    """Graphql queries."""

    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(  # noqa: WPS215
    ProjectsMutations,
    UsersMutations,
    BillingMutations,
    MediaMutations,
    graphene.ObjectType,
):
    """Graphql mutations."""


schema = scheme.Schema(query=Query, mutation=Mutation)


def get_api_graphql_view():
    """Provide graphql api view."""
    return ApiGraphQLView.as_view(schema=schema)


def get_graphql_view():
    """Provide graphql playground view."""
    return PlaygroundGraphQLView.as_view(graphiql=True, schema=schema)
