from dataclasses import dataclass
from typing import TypeAlias, TYPE_CHECKING

from .plugin_info import PluginInfo, PluginId


if TYPE_CHECKING:
    from .machinery.loader import PluginLoaderInfo


API_ATTRIBUTE_NAME = "__api__"


PluginAPI: TypeAlias = object


@dataclass
class Plugin:
    info: PluginInfo
    loader: "PluginLoaderInfo"
    enabled: bool
    api: PluginAPI | None


__all__ = [
    "Plugin",
    "PluginId",
    "PluginInfo",
]
