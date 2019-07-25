import graphene
from graphene_django.debug import DjangoDebug

from apps.core.graphql.views import (
    PrivateGraphQLView, DrfAuthenticatedGraphQLView
)
from apps.projects.graphql.queries import ProjectsQueries
from apps.projects.graphql.mutations import ProjectMutations
from apps.users.graphql.mutations import AuthMutations
from apps.users.graphql.queries import UsersQueries


class Query(ProjectsQueries,
            UsersQueries,
            graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')


class Mutation(ProjectMutations,
               AuthMutations,
               graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)


def get_api_graphql_view():
    return DrfAuthenticatedGraphQLView.as_view(
        schema=schema
    )


def get_graphql_view():
    return PrivateGraphQLView.as_view(
        graphiql=True,
        schema=schema
    )
