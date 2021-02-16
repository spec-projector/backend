from graphene_django.rest_framework.tests.test_mutation import mock_info

from apps.projects.graphql.resolvers import resolve_token_integration


def test_resolve_token(
    project,
    figma_integration,
    github_integration,
    gitlab_integration,
):
    """Test resolve filled tokens."""
    integrations = (figma_integration, github_integration, gitlab_integration)

    for integration in integrations:
        assert resolve_token_integration(integration, mock_info()) == "*"


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

        assert not resolve_token_integration(integration, mock_info())
