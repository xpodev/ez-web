from pydantic import BaseModel
from pathlib import Path
from typing import TypeAlias, ClassVar

from ..plugin import Plugin, PluginId


PluginLoaderId: TypeAlias = str


class PluginLoaderInfo(BaseModel):
    id: PluginLoaderId
    name: str


class IPluginLoader:
    info: ClassVar[PluginLoaderInfo]

    def __init__(self, plugin_dir: str) -> None:
        self._plugin_dir = Path(plugin_dir)

    @property
    def plugin_dir(self) -> Path:
        return self._plugin_dir

    def load(self, plugin_id: PluginId, plugin: Plugin | None) -> Plugin | None:
        raise NotImplementedError
    
    def run_main(self, plugin: Plugin) -> None:
        return None
