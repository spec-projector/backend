from rest_framework import serializers


class CreateProjectInput(serializers.Serializer):
    """Create project input."""

    title = serializers.CharField()
    isPublic = serializers.BooleanField(  # noqa: WPS115 N815
        source="is_public",
        default=False,
    )
