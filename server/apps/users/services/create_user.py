from dataclasses import asdict

from apps.users.logic.interfaces import IUserService
from apps.users.logic.interfaces.create_user import CreateUserData
from apps.users.models import User


class UserService(IUserService):
    """Service for create new user."""

    def create_user(self, user_data: CreateUserData) -> User:
        """Create new user by provided data."""
        return User.objects.create(is_staff=False, **asdict(user_data))
