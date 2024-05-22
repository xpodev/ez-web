from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from modules.plugins.plugin import Plugin, PluginInfo, PluginId, PluginAPI
    from modules.plugins.machinery.installer import IPluginInstaller, PluginInstallerInfo, PluginInstallerId
    from modules.plugins.machinery.loader import IPluginLoader, PluginLoaderInfo

    from modules.plugins.errors import EZPluginError, UnknownPluginError, DuplicateIDError
    from .events import Plugins

    from modules.plugins.manager import PLUGIN_MANAGER as __pm
    from modules.plugins.config import PLUGINS_PUBLIC_API_MODULE_NAME

    from modules.plugins.framework.settings import Settings
else:
    from ..plugin import Plugin, PluginInfo, PluginId, PluginAPI
    from ..machinery.installer import IPluginInstaller, PluginInstallerInfo, PluginInstallerId
    from ..machinery.loader import IPluginLoader, PluginLoaderInfo

    from .errors import EZPluginError, UnknownPluginError, DuplicateIDError
    from .events import Plugins

    from ..manager import PLUGIN_MANAGER as __pm
    from ..config import PLUGINS_PUBLIC_API_MODULE_NAME

    from ..framework.settings import Settings


def get_plugins() -> list[Plugin]:
    return __pm.get_plugins()


def get_plugin(plugin_id: PluginId) -> Plugin:
    return __pm.get_plugin(plugin_id)


def install(path: str, *, installer: PluginInstallerId | None = None):
    return __pm.install(path, installer=installer)


def uninstall(plugin_id: PluginId):
    __pm.uninstall(plugin_id)


def enable(plugin_id: PluginId) -> bool:
    if is_enabled(plugin_id):
        return False
    return __pm.enable(plugin_id) is None


def disable(plugin_id: PluginId) -> bool:
    if is_disabled(plugin_id):
        return False
    return __pm.disable(plugin_id) is None


def is_enabled(plugin_id: PluginId) -> bool:
    plugin = __pm.get_plugin(plugin_id)
    return plugin.enabled


def is_disabled(plugin_id: PluginId) -> bool:
    return not is_enabled(plugin_id)


def has_api(plugin_id: PluginId) -> bool:
    return get_api(plugin_id) is not None


def get_api(plugin_id: PluginId) -> PluginAPI | None:
    plugin = get_plugin(plugin_id)
    return plugin.api


def get_plugins_directory() -> str:
    return str(__pm.plugin_dir)


def get_plugin_public_api_module_name() -> str:
    return PLUGINS_PUBLIC_API_MODULE_NAME


def expose(plugin: Plugin, api: PluginAPI):
    return __pm.expose(plugin, api)


def add_installer(installer: IPluginInstaller | Callable[[str], IPluginInstaller]) -> IPluginInstaller:
    return __pm.add_installer(installer)


def remove_installer(installer: IPluginInstaller) -> bool:
    return __pm.remove_installer(installer)


def add_loader(loader: IPluginLoader | Callable[[str], IPluginLoader]) -> IPluginLoader:
    return __pm.add_loader(loader)


def remove_loader(loader: IPluginLoader) -> bool:
    return __pm.remove_loader(loader)


def get_installers() -> list[PluginInstallerInfo]:
    return [
        installer.info for installer in __pm.get_installers()
    ]


def get_loaders() -> list[PluginLoaderInfo]:
    return [
        loader.info for loader in __pm.get_loaders()
    ]


__all__ = [
    "Plugin",
    "IPluginInstaller",
    "PluginInstallerInfo",
    "IPluginLoader",
    "PluginLoaderInfo",
    "UnknownPluginError",
    "DuplicateIDError",
    "PluginInfo",
    "EZPluginError",
    "Plugins",
    "Settings",
    "get_plugins",
    "get_plugin",
    "install",
    "uninstall",
    "enable",
    "disable",
    "is_enabled",
    "is_disabled",
    "has_api",
    "get_api",
    "get_plugins_directory",
    "get_plugin_public_api_module_name",
    "expose",
    "add_installer",
    "remove_installer",
    "add_loader",
    "remove_loader",
    "get_installers",
    "get_loaders",
]
