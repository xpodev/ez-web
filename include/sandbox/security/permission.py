from enum import IntFlag


class Permission(IntFlag):
    ...


class PermissionSet:
    _types: dict[type[Permission], Permission]

    def __init__(self, *permissions: Permission):
        self._types = {
            permission_type: permission_type(0) for permission_type in set(map(type, permissions))
        }
        for permission in permissions:
            self._types[type(permission)] |= permission
        
    def __getitem__(self, permission_type: type[Permission]) -> Permission:
        return self._types[permission_type]

    def __contains__(self, permission: Permission) -> bool:
        try:
            return bool(self._types[type(permission)] & permission)
        except KeyError:
            return False
    
    def __and__(self, other: "PermissionSet") -> "PermissionSet":
        return PermissionSet(
            *(
                permission
                for permission in self._types.values()
                if permission in other
            )
        )
    
    def __or__(self, other: "PermissionSet") -> "PermissionSet":
        return PermissionSet(
            *(
                permission
                for permission in self._types.values()
                if permission in other
            )
        )
