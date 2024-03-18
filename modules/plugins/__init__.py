from .machinery.manager import PluginManager
from .builtins.installer import EZPluginInstaller
from .builtins.loader import EZPluginLoader

from .config import PLUGINS_DIRECTORY

from . import manager


def init_manager(host, oid):
    manager.PLUGIN_MANAGER = PluginManager(
        host, 
        oid, 
        str(PLUGINS_DIRECTORY), 
        EZPluginInstaller, 
        EZPluginLoader
    )
    manager.PLUGIN_MANAGER.enable_public_api()
    return manager.PLUGIN_MANAGER


__app_class__ = init_manager
