import graphene


class UserAccessTokenCreatedType(graphene.ObjectType):
    """User access token created type."""

    id = graphene.ID()
    key = graphene.String()
    name = graphene.String()
    created_at = graphene.DateTime()
