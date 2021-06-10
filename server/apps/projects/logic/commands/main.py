from apps.projects.logic.commands.project import create as create_project
from apps.projects.logic.commands.project import delete as delete_project
from apps.projects.logic.commands.project import update as update_project
from apps.projects.logic.commands.project_asset import (
    create as create_project_assets,
)

COMMANDS = (
    (
        create_project_assets.Command,
        create_project_assets.CommandHandler,
    ),
    (
        delete_project.Command,
        delete_project.CommandHandler,
    ),
    (
        update_project.Command,
        update_project.CommandHandler,
    ),
    (
        create_project.Command,
        create_project.CommandHandler,
    ),
)
