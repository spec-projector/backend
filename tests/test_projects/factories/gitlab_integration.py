import factory

from apps.projects.models import GitLabIntegration
from tests.test_projects.factories.project import ProjectFactory


class GitLabIntegrationFactory(factory.django.DjangoModelFactory):
    """GitLab integration factory."""

    class Meta:
        model = GitLabIntegration

    project = factory.SubFactory(ProjectFactory)
    token = factory.Sequence(lambda index: "gitlab_{0}".format(index))
