from .projects import CreateProject, UpdateProject, DeleteProject


class ProjectMutations:
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
