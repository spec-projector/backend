from collections import OrderedDict

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "COUCHDB_URL": ("http://couchdb:5984", "", str),
    "COUCHDB_USER": ("", "", str),
    "COUCHDB_PASSWORD": ("", "", str),

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
    ),
)
