from apps.projects.services.issues.meta import IssueMeta, System
from apps.projects.services.issues.providers import (
    DummyProvider,
    GithubProvider,
    GitlabProvider,
)

Providers = [
    GithubProvider,
    GitlabProvider,
    DummyProvider,
]

PROVIDERS = {  # noqa: WPS407
    system: provider for system, provider in zip(System, Providers)
}


def get_issue(url: str, token: str, system: System) -> IssueMeta:
    """Get issue from remote provider."""
    provider = PROVIDERS[system]
    return provider(token).get_issue(url)
