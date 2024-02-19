from .machinery.manager import PluginManager
from .builtins.installer import EZPluginInstaller
from .builtins.loader import EZPluginLoader

from .config import PLUGINS_DIRECTORY

PLUGIN_MANAGER = PluginManager(PLUGINS_DIRECTORY, EZPluginInstaller, EZPluginLoader)
PLUGIN_MANAGER.enable_public_api()
