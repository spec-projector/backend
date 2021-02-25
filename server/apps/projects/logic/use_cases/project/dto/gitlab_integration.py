from dataclasses import dataclass

from rest_framework import serializers


class GitLabIntegrationDtoValidator(serializers.Serializer):
    """GitLab integration validator."""

    token = serializers.CharField(required=False)


@dataclass(frozen=True)
class GitLabIntegrationDto:
    """GitLab integration data."""

    token: str
