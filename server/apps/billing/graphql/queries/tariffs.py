import graphene

from apps.billing.graphql.fields import TariffConnectionField


class TariffsQueries(graphene.ObjectType):
    """Graphql tariffs queries."""

    all_tariffs = TariffConnectionField()
