from typing import Any

from sandbox.host import AppHost

from ..module_manager import ModuleManager, ModuleManagerConfig
from ..web import EZWebApplication


class EZApplication:
    web_app: EZWebApplication
    app_host: AppHost
    module_manager: ModuleManager

    def __init__(self) -> None:
        self._host = self.app_host = AppHost(self)

        from sandbox.events.event_emitter import EventEmitter

        self.web_app = EZWebApplication()
        self.event_system = EventEmitter(self.app_host)

        module_manager_config = ModuleManagerConfig()
        self.module_manager = ModuleManager(self.app_host, module_manager_config)

    def run(self) -> Any:
        self.module_manager.load_modules()

        import ez.log as log

        for module in self.module_manager.get_modules():
            log.info(f"\tLoaded module: {module.name}")

        self.event_system.emit("App.Started")
