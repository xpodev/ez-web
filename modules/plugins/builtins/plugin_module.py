from types import ModuleType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ez.plugins import Plugin, PluginInfo


class PluginModule(ModuleType):
    __plugin__: "Plugin"
    __info__: "PluginInfo"

    def __init__(self, name, doc=None):
        super().__init__(name, doc)
        self.__path__ = []
        self.__package__ = name

    def __repr__(self):
        return f"<PluginModule '{self.__name__}'>"
