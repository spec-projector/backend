import injector

from apps.users import services
from apps.users.logic import interfaces


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
            interfaces.IAuthenticationService,
            services.AuthenticationService,
            scope=injector.singleton,
        )
        binder.bind(
            interfaces.ISocialLoginService,
            services.SocialLoginService,
            scope=injector.singleton,
        )
        binder.bind(
            interfaces.IResetPasswordRequestService,
            services.ResetPasswordRequestService,
            scope=injector.singleton,
        )
        binder.bind(
            interfaces.IUserService,
            services.UserService,
            scope=injector.singleton,
        )
