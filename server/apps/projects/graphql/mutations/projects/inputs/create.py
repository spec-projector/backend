from rest_framework import serializers


class CreateProjectInput(serializers.Serializer):
    """Create project input."""

    title = serializers.CharField()
