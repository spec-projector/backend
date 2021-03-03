from collections import OrderedDict

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

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
    ),
)
