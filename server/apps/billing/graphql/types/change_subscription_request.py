import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.billing.graphql.types import SubscriptionType, TariffType
from apps.billing.models import ChangeSubscriptionRequest


class ChangeSubscriptionRequestType(BaseModelObjectType):
    """ChangeSubscriptionRequest graphql type."""

    class Meta:
        model = ChangeSubscriptionRequest
        auth_required = True

    created_at = graphene.DateTime(required=True)
    is_active = graphene.Boolean(required=True)
    tariff = graphene.Field(TariffType, required=True)
    from_subscription = graphene.Field(SubscriptionType)
    to_subscription = graphene.Field(SubscriptionType)
