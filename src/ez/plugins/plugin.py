from types import ModuleType
from .plugin_info import PluginInfo


API_ATTRIBUTE_NAME = "__api__"


class Plugin:
    info: PluginInfo
    module: ModuleType

    def __init__(self, info: PluginInfo, module: ModuleType):
        self.info = info
        self.module = module

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
