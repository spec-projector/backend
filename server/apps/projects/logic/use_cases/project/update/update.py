from typing import Type

import injector
from django.db import models
from rest_framework import exceptions

from apps.billing.logic.interfaces import ITariffLimitsService
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.use_cases import BaseUseCase
from apps.core.utils.objects import empty
from apps.projects.logic.use_cases.project.update.dto import (
    InputDto,
    OutputDto,
    ProjectDtoValidator,
)
from apps.projects.models import (
    FigmaIntegration,
    GitHubIntegration,
    GitLabIntegration,
    Project,
)
from apps.projects.models.project_member import ProjectMember


class UseCase(BaseUseCase):
    """Use case for updating projects."""

    @injector.inject
    def __init__(
        self,
        tariff_limits_service: ITariffLimitsService,
    ):
        """Initialize."""
        self._tariff_limits_service = tariff_limits_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        project = Project.objects.filter(pk=input_dto.project).first()
        if not project:
            raise exceptions.ValidationError("Project not found")

        validated_data = validate_input(
            input_dto.data,
            ProjectDtoValidator,
        )
        members = validated_data.pop("users", None)
        if members is not None:
            self._tariff_limits_service.assert_project_member_count_allowed(
                project,
                len(members),
            )
            self._update_members(project, members)

        self._update_figma_integration(project, validated_data)
        self._update_github_integration(project, validated_data)
        self._update_gitlab_integration(project, validated_data)

        for field, field_value in validated_data.items():
            setattr(project, field, field_value)
        project.save()

        return OutputDto(project=project)

    def _update_members(self, project, members) -> None:
        project_members = []
        for project_member_input in members:
            project_member, _ = ProjectMember.objects.update_or_create(
                project=project,
                user=project_member_input["id"],
                defaults={"roles": project_member_input.get("roles")},
            )

            project_members.append(project_member)

        for member in ProjectMember.objects.filter(project=project):
            if member not in project_members:
                member.delete()

    def _update_figma_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            FigmaIntegration,
            "figma_integration",
        )

    def _update_github_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            GitHubIntegration,
            "github_integration",
        )

    def _update_gitlab_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            GitLabIntegration,
            "gitlab_integration",
        )

    def _update_integration(
        self,
        project: Project,
        validated_data,
        model: Type[models.Model],
        field: str,
    ):
        integration_dto = validated_data.pop(field, empty)
        if integration_dto != empty:
            if integration_dto:
                model.objects.update_or_create(
                    project=project,
                    defaults={"token": integration_dto["token"]},
                )
            elif integration_dto is None:
                model.objects.filter(project=project).delete()
