def backend_is_valid(backend_name: str, **kwargs) -> bool:
    """
    Check valid backend.

    Check from here:
    social_core.backends.base.BaseAuth.authenticate.
    """
    required_fields = ("backend", "strategy", "response")
    for required_field in required_fields:
        if required_field not in kwargs:
            return False

    return kwargs["backend"].name == backend_name
