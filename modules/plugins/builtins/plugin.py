from dataclasses import dataclass

from ..plugin import Plugin
from .plugin_module import PluginModule

    
@dataclass
class EZPlugin(Plugin):
    module: PluginModule | None

    @property
    def is_loaded(self):
        return self.module is not None
