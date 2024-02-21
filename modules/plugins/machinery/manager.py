from typing import Callable
from types import ModuleType
from pathlib import Path

from ..machinery.installer import PluginInstallerId
from ..machinery.loader import PluginLoaderId

from ..plugin import (
    Plugin, 
    PluginInfo, 
    PluginId,
)

from ..errors import (
    UnknownPluginError,
    UnknownPluginInstallerError,
    UnknownPluginLoaderError,
    DuplicateIDError,
)

from ..machinery.installer import IPluginInstaller
from ..machinery.loader import IPluginLoader

from ..config import PLUGINS_PUBLIC_API_MODULE_NAME


class PluginManager:
    EZ_PLUGIN_PREFIX = "ez.current-site.plugins"

    def __init__(
            self, 
            plugin_dir: str, 
            default_installer: Callable[[str], IPluginInstaller] | IPluginInstaller,
            default_loader: Callable[[str], IPluginLoader] | IPluginLoader,
            public_api: ModuleType | None = None
            ) -> None:
        self.plugin_dir = Path(plugin_dir)
        self._plugins: dict[PluginId, Plugin] = {}
        self._plugin_installers: dict[PluginInstallerId, IPluginInstaller] = {}
        self._plugin_loaders: dict[PluginLoaderId, IPluginLoader] = {}

        self._default_plugin_installer = self.add_installer(default_installer)
        self._default_plugin_loader = self.add_loader(default_loader)

        self._public_api = public_api or ModuleType(PLUGINS_PUBLIC_API_MODULE_NAME)

        self._current_plugin: PluginId = None

    #region Plugin Public API

    @property
    def public_api(self):
        return self._public_api
    
    def enable_public_api(self, alias: str = None):
        alias = alias or PLUGINS_PUBLIC_API_MODULE_NAME

        import sys

        sys.modules[alias] = self._public_api
        self._public_api.__ez_name__ = alias

    def disable_public_api(self):
        import sys

        del sys.modules[self._public_api.__ez_name__]

    def expose(self, plugin: Plugin, api: object):
        if api is None:
            raise ValueError("API cannot be None")
        
        api_name = plugin.info.package_name.replace("-", "_")
        if hasattr(self._public_api, api_name):
            raise ValueError(f"API name {api_name} already in use")

        plugin.api = api
        setattr(self._public_api, api_name, api)

    #endregion

    def get_plugin(self, plugin_id: PluginId) -> Plugin:
        try:
            return self._plugins[plugin_id]
        except KeyError:
            raise UnknownPluginError(plugin_id) from None

    def get_plugins(self):
        return list(self._plugins.values())

    #region Installers & Loaders
    
    def add_installer(self, installer: IPluginInstaller | Callable[[str], IPluginInstaller]) -> IPluginInstaller:
        if not isinstance(installer, IPluginInstaller):
            installer = installer(self.plugin_dir)
        if installer.info.id in self._plugin_installers:
            raise DuplicateIDError(installer, installer.info.id)
        self._plugin_installers[installer.info.id] = installer
        return installer

    def add_loader(self, loader: IPluginLoader | Callable[[str], IPluginLoader]) -> IPluginLoader:
        if not isinstance(loader, IPluginInstaller):
            loader = loader(self.plugin_dir)
        if loader.info.id in self._plugin_loaders:
            raise DuplicateIDError(loader, loader.info.id)
        self._plugin_loaders[loader.info.id] = loader
        return loader

    def remove_installer(self, installer: IPluginInstaller) -> bool:
        try:
            del self._plugin_installers[installer.info.id]
        except KeyError:
            return False
        return True

    def remove_loader(self, loader: IPluginLoader) -> bool:
        try:
            del self._plugin_loaders[loader.info.id]
        except KeyError:
            return False
        return True
    
    def get_installer(self, installer: PluginInstallerId) -> IPluginInstaller:
        try:
            return self._plugin_installers[installer]
        except KeyError:
            raise UnknownPluginInstallerError(installer) from None
        
    def get_loader(self, loader: PluginLoaderId) -> IPluginLoader:
        try:
            return self._plugin_loaders[loader]
        except KeyError:
            raise UnknownPluginLoaderError(loader) from None
        
    def get_installers(self):
        return list(self._plugin_installers.values())
    
    def get_loaders(self):
        return list(self._plugin_loaders.values())
    
    #endregion

    #region Installation

    def install(self, path: str, *, installer: PluginInstallerId = None):
        if installer is None:
            _installer = self._default_plugin_installer
        else:
            _installer = self.get_installer(installer)
        return _installer.install(path)
    
    def uninstall(self, plugin_id: PluginId):
        plugin = self.get_plugin(plugin_id)
        installer = self.get_installer(plugin.info.installer_id)
        installer.uninstall(plugin_id)

    #endregion

    #region Plugin Status
        
    @property
    def current_plugin(self):
        return self._current_plugin
        
    def enable(self, plugin_id: PluginId):
        ...

    def disable(self, plugin_id: PluginId):
        ...

    def load_plugin(self, plugin_id: PluginId):
        loader = self._default_plugin_loader

        try:
            plugin = self.get_plugin(plugin_id)
        except UnknownPluginError:
            plugin = loader.load(plugin_id, None)

            if plugin is None:
                raise TypeError(f"Plugin loader {loader.info.id} returned None for plugin {plugin_id}")
            self._plugins[plugin_id] = plugin

            if plugin.api is not None:
                self.expose(plugin, plugin.api)
        else:
            loader.load(plugin_id, plugin)
        
        return plugin

    def load_plugins(self, *plugin_ids: PluginId):
        for plugin_id in plugin_ids:
            self._current_plugin = plugin_id
            self.load_plugin(plugin_id)

    def run_plugins(self, *plugin_ids: PluginId):
        if not plugin_ids:
            plugin_ids = self._plugins.keys()
        for plugin_id in plugin_ids:
            plugin = self.get_plugin(plugin_id)
            loader = self.get_loader(plugin.loader.id)
            self._current_plugin = plugin_id
            loader.run_main(plugin)

    #endregion

    @classmethod
    def get_plugin_full_name(cls, plugin: str | PluginInfo) -> str:
        if isinstance(plugin, PluginInfo):
            plugin = plugin.package_name
        return f"{cls.EZ_PLUGIN_PREFIX}.{plugin}"
