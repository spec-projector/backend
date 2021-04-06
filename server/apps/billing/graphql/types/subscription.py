import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.billing.graphql.types import TariffType
from apps.billing.models import Subscription


class SubscriptionType(BaseModelObjectType):
    """Subscription graphql type."""

    class Meta:
        model = Subscription

    created = graphene.DateTime()
    tariff = graphene.Field(TariffType)
    active_until = graphene.DateTime()
