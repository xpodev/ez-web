from typing import TYPE_CHECKING

from ..identity import ObjectIDBase, ObjectID
from ..security.security_provider import SecurityProvider, PermissionSet

if TYPE_CHECKING:
    from ..host import AppHost


class Application(ObjectIDBase, SecurityProvider):
    _host: "AppHost | None"

    def __init__(self, oid: ObjectID, permissions: PermissionSet) -> None:
        ObjectIDBase.__init__(self, oid)
        SecurityProvider.__init__(self, permissions)
        self._host = None

    @property
    def is_root(self):
        if self.host is None:
            return False
        return self.host.root_application == self

    @property
    def host(self) -> "AppHost | None":
        return self._host

    def __repr__(self):
        return f"<Application {self.oid}>"
