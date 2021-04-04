from dataclasses import dataclass

from rest_framework import serializers

from apps.projects.logic.interfaces.issues import IssuesManagementSystem
from apps.projects.models import Project


class IssueDtoValidator(serializers.Serializer):
    """Create issue input dto validator."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )
    url = serializers.CharField()
    system = serializers.ChoiceField(choices=IssuesManagementSystem)


@dataclass(frozen=True)
class InputDto:
    """Create issue input dto."""

    project: str
    url: str
    system: IssuesManagementSystem
