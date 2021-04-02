import graphene
from jnt_django_graphene_toolbox.nodes import ModelRelayNode

from apps.billing.graphql.fields import TariffConnectionField
from apps.billing.graphql.types import TariffType


class TariffsQueries(graphene.ObjectType):
    """Graphql tariffs queries."""

    tariff = ModelRelayNode.Field(TariffType)
    all_tariffs = TariffConnectionField()
