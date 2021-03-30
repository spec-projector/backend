from django import forms

from apps.users.admin.validators import LoginValidator
from apps.users.models import User


class UserForm(forms.ModelForm):
    """Main user form."""

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs) -> None:
        """Initialize user change form."""
        super().__init__(*args, **kwargs)
        self._update_login()

    def _update_login(self) -> None:
        """Add login validator."""
        login_field = self.fields.get("login")
        if login_field:
            login_field.validators.append(LoginValidator())
