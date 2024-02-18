from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from ..plugin import Plugin
from ..plugin_info import PluginId


PluginLoaderId: TypeAlias = str


@dataclass
class PluginLoaderInfo:
    id: PluginLoaderId
    name: str


class IPluginLoader:
    info: PluginLoaderInfo

    def __init__(self, plugin_dir: str) -> None:
        self._plugin_dir = Path(plugin_dir)

    @property
    def plugin_dir(self) -> Path:
        return self._plugin_dir

    def load(self, plugin_id: PluginId, plugin: Plugin | None) -> Plugin | None:
        raise NotImplementedError
    
    def run_main(self, plugin: Plugin) -> None:
        return None
