from typing import TYPE_CHECKING

from starlette.applications import Starlette

if TYPE_CHECKING:
    from sandbox.host import AppHost


class EZWebApplication(Starlette):
    def __init__(self, app_host: "AppHost"):
        Starlette.__init__(self)
        self.app_host = app_host
