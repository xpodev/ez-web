from .permission import PermissionSet


class SecurityProvider:
    _permissions: PermissionSet

    def __init__(self, permissions: PermissionSet):
        self._permissions = permissions

    @property
    def permissions(self) -> PermissionSet:
        return self._permissions
