# -*- coding: utf-8 -*-

from apps.projects.graphql.mutations.projects import create, delete, update


class ProjectsMutations:
    """All projects mutations."""

    create_project = create.CreateProjectMutation.Field()
    update_project = update.UpdateProjectMutation.Field()
    delete_project = delete.DeleteProjectMutation.Field()
