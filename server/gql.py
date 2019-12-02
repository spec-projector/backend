import graphene
from graphene_django.debug import DjangoDebug

from apps.core.graphql.views import (ApiGraphQLView, PlaygroundGraphQLView)
from apps.projects.graphql.mutations import ProjectMutations
from apps.projects.graphql.queries import ProjectsQueries
from apps.users.graphql.mutations import AuthMutations
from apps.users.graphql.queries import UsersQueries


class Query(
    ProjectsQueries,
    UsersQueries,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(
    ProjectMutations,
    AuthMutations,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)


def get_api_graphql_view():
    return ApiGraphQLView.as_view(
        schema=schema
    )


def get_graphql_view():
    return PlaygroundGraphQLView.as_view(
        graphiql=True,
        schema=schema
    )
