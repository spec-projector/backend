from graphene_django.rest_framework.tests.test_mutation import mock_info

from apps.projects.graphql.types.base import BaseIntegrationType


def test_resolve_token(
    project,
    figma_integration,
    github_integration,
    gitlab_integration,
):
    """Test resolve filled tokens."""
    integrations = (figma_integration, github_integration, gitlab_integration)

    for integration in integrations:
        assert (
            BaseIntegrationType.resolve_token(integration, mock_info()) == "*"
        )


def test_resolve_empty_tokens(
    project,
    figma_integration,
    github_integration,
    gitlab_integration,
):
    """Test resolve not filled tokens."""
    integrations = (figma_integration, github_integration, gitlab_integration)

    for integration in integrations:
        integration.token = ""
        integration.save()

        assert (
            BaseIntegrationType.resolve_token(integration, mock_info()) is None
        )
