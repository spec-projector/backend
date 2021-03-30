from django.contrib.auth.forms import UserCreationForm

from apps.users.admin.validators import LoginValidator


class UserCreateForm(UserCreationForm):
    """Main user create form."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize user create form."""
        super().__init__(*args, **kwargs)
        self._update_login()

    def _update_login(self) -> None:
        """Add login validator."""
        login_field = self.fields.get("login")
        if login_field:
            login_field.validators.append(LoginValidator())
