from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .machinery.manager import PluginManager


PLUGIN_MANAGER: "PluginManager"
