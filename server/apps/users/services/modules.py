import injector

from apps.users import services
from apps.users.logic import interfaces
from apps.users.services.auth.logout import LogoutService
from apps.users.services.auth.social_login import SocialLoginService


class UserInfrastructureModule(injector.Module):
    """Setup di for user services."""

    def configure(self, binder: injector.Binder) -> None:
        """Bind services."""
        binder.bind(
            interfaces.ITokenService,
            services.TokenService,
            scope=injector.singleton,
        )
        binder.bind(
            interfaces.ILoginService,
            services.LoginService,
            scope=injector.singleton,
        )
        binder.bind(LogoutService, scope=injector.singleton)
        binder.bind(SocialLoginService, scope=injector.singleton)
