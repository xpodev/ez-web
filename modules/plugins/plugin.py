from types import ModuleType
from .plugin_info import PluginInfo


API_ATTRIBUTE_NAME = "__api__"


class Plugin:
    info: PluginInfo
    module: ModuleType | None
    enabled: bool

    def __init__(self, info: PluginInfo, module: ModuleType | None):
        self.info = info
        self.module = module
        self.enabled = False

    @property
    def is_loaded(self) -> bool:
        return self.module is not None

    @property
    def name(self) -> str:
        return self.info.name
    
    @property
    def version(self) -> str:
        return str(self.info.version)
    
    @property
    def has_api(self) -> bool:
        return hasattr(self.module, API_ATTRIBUTE_NAME)
    
    @property
    def api(self):
        return getattr(self.module, API_ATTRIBUTE_NAME, None)
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
