# -*- coding: utf-8 -*-

from enum import Enum

from apps.projects.graphql.types import IssueType
from apps.projects.services.issues.providers import (
    DummyProvider,
    GithubProvider,
    GitlabProvider,
)

System = Enum('System', ('GITHUB', 'GITLAB', 'DUMMY'))
Providers = [GithubProvider, GitlabProvider, DummyProvider]

PROVIDERS = {  # noqa: WPS407
    system.value: provider for system, provider in zip(System, Providers)
}


def get_issue(url: str, token: str, system: System) -> IssueType:
    provider = PROVIDERS[system]
    return provider(url, token).get_issue()
