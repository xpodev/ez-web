import ez.lowlevel

from .machinery.manager import PluginManager
from .builtins.installer import EZPluginInstaller
from .builtins.loader import EZPluginLoader

from .config import PLUGINS_DIRECTORY

from . import manager


def init_manager(host):
    manager.PLUGIN_MANAGER = PluginManager(
        host, 
        str(PLUGINS_DIRECTORY), 
        EZPluginInstaller, 
        EZPluginLoader
    )
    manager.PLUGIN_MANAGER.enable_public_api()
    return manager.PLUGIN_MANAGER


init_manager(ez.lowlevel.APP_HOST)

__deps__ = [
    "events"
]
