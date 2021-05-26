import graphene
from jnt_django_graphene_toolbox.fields import BitField
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.billing.models import Tariff
from apps.billing.models.enums import TariffFeatures


class TariffType(BaseModelObjectType):
    """Tariff graphql type."""

    class Meta:
        model = Tariff

    order = graphene.Int()
    code = graphene.String()
    title = graphene.String()
    teaser = graphene.String()
    icon = graphene.String()
    price = graphene.Float()
    is_active = graphene.Boolean()
    features = BitField(TariffFeatures)
    max_projects = graphene.Int()
    max_project_members = graphene.Int()
