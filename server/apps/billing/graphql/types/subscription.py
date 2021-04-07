import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.billing.graphql.types import TariffType
from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus


class SubscriptionType(BaseModelObjectType):
    """Subscription graphql type."""

    class Meta:
        model = Subscription

    created_at = graphene.DateTime(required=True)
    tariff = graphene.Field(TariffType, required=True)
    active_until = graphene.DateTime()
    status = graphene.Enum.from_enum(SubscriptionStatus)(required=True)
