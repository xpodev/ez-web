from typing import Any

from sandbox.applications import Application
from sandbox.host import AppHost, AppHostPermission
from sandbox.events.event_emitter import EventEmitter
from sandbox.security import PermissionSet

from ..module_manager import ModuleManager, ModuleManagerConfig
from ..web import EZWebApplication


class EZApplication(Application):
    web_app: EZWebApplication
    app_host: AppHost
    event_system: EventEmitter
    module_manager: ModuleManager

    def __init__(self) -> None:
        super().__init__("ez", PermissionSet(
            AppHostPermission.CreateApplications, 
            AppHostPermission.ManageApplications
        ))

        self._host = self.app_host = AppHost(self)

        self.web_app = self.app_host.create_application(EZWebApplication)
        self.event_system = self.app_host.create_application(EventEmitter)

        module_manager_config = ModuleManagerConfig()
        self.module_manager = self.app_host.create_application(
            ModuleManager, 
            module_manager_config,
            PermissionSet(
                AppHostPermission.CreateApplications,
                AppHostPermission.ManageApplications
            )
        )

    def run(self) -> Any:
        with self.app_host.application(self.event_system):
            self.event_system.setup()
        with self.app_host.application(self.module_manager):
            self.module_manager.load_modules()
