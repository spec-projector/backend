from apps.billing.logic.services.subscription import NoActiveSubscriptionError
from apps.core.graphql.errors import GenericGraphQLError
from apps.projects.models import ProjectMember
from apps.projects.models.enums import ProjectPermission
from apps.projects.models.project_member import ProjectMemberRole
from tests.helpers.bit_field import assert_bitfield
from tests.test_projects.factories.project_member import ProjectMemberFactory
from tests.test_users.factories.user import UserFactory


def test_delete_project_members(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test delete project members."""
    project_member1 = ProjectMemberFactory.create(project=project)
    project_member2 = ProjectMemberFactory.create(project=project)

    assert project.members.count() == 2

    users = [
        {
            "id": project_member1.user.id,
            "role": ProjectMemberRole.VIEWER,
            "permissions": [ProjectPermission.EDIT_MODULES],
        },
    ]

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )

    assert project.members.count() == 1
    assert project.members.first() == project_member1.user
    assert not ProjectMember.objects.filter(id=project_member2.id).exists()


def test_add_project_members(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test add project members."""
    user2 = UserFactory.create()
    user3 = UserFactory.create()

    users = [
        {
            "id": user2.id,
            "role": ProjectMemberRole.EDITOR,
            "permissions": [ProjectPermission.EDIT_FEATURE_API],
        },
        {
            "id": user3.id,
            "role": ProjectMemberRole.VIEWER,
            "permissions": [
                ProjectPermission.EDIT_SPRINTS,
                ProjectPermission.EDIT_MODULES,
            ],
        },
    ]

    assert not project.members.exists()

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )

    members = {
        member.user: member
        for member in ProjectMember.objects.filter(project=project)
    }
    assert len(members) == 2
    assert set(members.keys()) == {user2, user3}

    assert_bitfield(
        members[user2].permissions,
        ProjectMember.permissions.EDIT_FEATURE_API,
    )

    assert_bitfield(
        members[user3].permissions,
        ProjectMember.permissions.EDIT_SPRINTS
        | ProjectMember.permissions.EDIT_MODULES,
    )


def test_update_without_subscription(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test update members without subscription."""
    user.subscriptions.all().delete()

    users = [
        {
            "id": UserFactory.create().id,
            "role": ProjectMemberRole.VIEWER,
            "permissions": [ProjectPermission.EDIT_SPRINTS],
        },
        {
            "id": UserFactory.create().id,
            "role": ProjectMemberRole.VIEWER,
            "permissions": [ProjectPermission.EDIT_SPRINTS],
        },
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "members": users,
        },
    )

    assert isinstance(response, GenericGraphQLError)
    assert isinstance(response.original_error, NoActiveSubscriptionError)
