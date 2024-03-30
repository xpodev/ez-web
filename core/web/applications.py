from typing import TYPE_CHECKING
from fastapi import FastAPI

from sandbox.applications import Application
from sandbox.security.permission import PermissionSet

if TYPE_CHECKING:
    from sandbox.host import AppHost


class EZWebApplication(Application, FastAPI):
    def __init__(self, app_host: "AppHost"):
        super().__init__("web", PermissionSet())
        FastAPI.__init__(self)
        self.app_host = app_host
        self._initialize()

    def _initialize(self):
        pass
