from dataclasses import dataclass

from rest_framework import serializers


class GitHubIntegrationDtoValidator(serializers.Serializer):
    """GitHub integration validator."""

    token = serializers.CharField(required=False)


@dataclass(frozen=True)
class GitHubIntegrationDto:
    """GitHub integration data."""

    token: str
