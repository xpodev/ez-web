from functools import wraps

from .errors import InsufficientPermissionsError
from .permission import Permission
from .security_provider import SecurityProvider


def has_permissions(provider: SecurityProvider, permissions: Permission) -> bool:
        return all(permission in provider.permissions for permission in permissions)


def requires(permissions: Permission):
    if not permissions:
         return lambda func: func

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from ..host import AppHost
            
            current_application = AppHost.current_host.current_application
            if current_application is AppHost.current_host.root_application:
                return func(*args, **kwargs)
            if not has_permissions(current_application, permissions):
                raise InsufficientPermissionsError(current_application, permissions)
            return func(*args, **kwargs)
        return wrapper
    return decorator
