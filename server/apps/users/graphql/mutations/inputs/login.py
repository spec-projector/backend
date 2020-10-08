from rest_framework import serializers


class LoginMutationInput(serializers.Serializer):
    """Login mutation input."""

    username = serializers.CharField()
    password = serializers.CharField()
