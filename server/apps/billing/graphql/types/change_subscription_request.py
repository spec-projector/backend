import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.billing.graphql.types import TariffType
from apps.billing.models import ChangeSubscriptionRequest
from apps.billing.models.enums import SubscriptionStatus


class ChangeSubscriptionRequestType(BaseModelObjectType):
    """ChangeSubscriptionRequest graphql type."""

    class Meta:
        model = ChangeSubscriptionRequest

    created_at = graphene.DateTime(required=True)
    is_active = graphene.Boolean(required=True)
    tariff = graphene.Field(TariffType, required=True)
    status = graphene.Enum.from_enum(SubscriptionStatus)(required=True)
