from collections import OrderedDict

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_ADDITIONAL_FIELDS = {
    "default_tariff": [
        "apps.core.admin.config.fields.TariffConfigField",
        {"model": "billing.Tariff", "field_name": "default_tariff"},
    ],
}

empty_default_str = ("", "", str)

CONSTANCE_CONFIG = {
    "COUCHDB_URL": ("http://couchdb:5984", "", str),
    "COUCHDB_USER": empty_default_str,
    "COUCHDB_PASSWORD": empty_default_str,
    # email
    "EMAIL_HOST": empty_default_str,
    "EMAIL_PORT": empty_default_str,
    "EMAIL_HOST_USER": empty_default_str,
    "EMAIL_HOST_PASSWORD": empty_default_str,
    "EMAIL_USE_TLS": (True, "", bool),
    "DEFAULT_FROM_EMAIL": empty_default_str,
    "CLOUD_PAYMENT_PUBLIC_ID": empty_default_str,
    "CLOUD_PAYMENT_API_SECRET": empty_default_str,
    "DEFAULT_TARIFF": (None, "Current default tariff", "default_tariff"),
}

CONSTANCE_CONFIG_FIELDSETS = OrderedDict(
    (
        (
            "CouchDB",
            (
                "COUCHDB_URL",
                "COUCHDB_USER",
                "COUCHDB_PASSWORD",
            ),
        ),
        (
            "Payment",
            (
                "CLOUD_PAYMENT_PUBLIC_ID",
                "CLOUD_PAYMENT_API_SECRET",
            ),
        ),
        (
            "Email",
            (
                "EMAIL_HOST",
                "EMAIL_PORT",
                "EMAIL_HOST_USER",
                "EMAIL_HOST_PASSWORD",
                "EMAIL_USE_TLS",
                "DEFAULT_FROM_EMAIL",
            ),
        ),
        ("Billing", ("DEFAULT_TARIFF",)),
    ),
)
