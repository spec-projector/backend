from apps.billing.graphql.queries import tariffs


class BillingQueries(
    tariffs.TariffsQueries,
):
    """All billing queries."""
