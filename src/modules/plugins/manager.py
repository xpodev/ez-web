import sys
from utilities.semver import SemanticVersion

from .plugin_info import PluginInfo
from .plugin import Plugin
from .errors import UnknownPluginError

from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from importlib import reload


class PluginManager:
    PLUGIN_PREFIX = "ez.current-site.plugins"

    def __init__(self, plugin_dir: Path) -> None:
        self.plugin_dir = plugin_dir
        self._plugins: dict[str, Plugin] = {}

    def enable_plugin(self, plugin_name: str):
        try:
            plugin = self._plugins[plugin_name]
        except KeyError:
            raise UnknownPluginError(plugin_name)
        else:
            if plugin.enabled:
                return
            plugin.enable()
            if plugin.is_loaded:
                reload(plugin.module)
            else:
                self.load_plugin(plugin)

    def disable_plugin(self, plugin_name: str):
        try:
            plugin = self._plugins[plugin_name]
        except KeyError:
            raise UnknownPluginError(plugin_name)
        else:
            if not plugin.enabled:
                return
            plugin.disable()

    def get_plugin_info(self, plugin_name: str) -> PluginInfo:
        return self._plugins[plugin_name].info
    
    def add_plugin(self, plugin: PluginInfo) -> None:
        self._plugins[plugin.dir_name] = Plugin(plugin, None)

    def load_plugin(self, plugin: str | PluginInfo, _plugin: Plugin | None = None) -> bool:
        if isinstance(plugin, str):
            try:
                plugin = self.get_plugin_info(plugin)
            except KeyError:
                dir_name = plugin
            else:
                dir_name = plugin.dir_name
        if dir_name in self._plugins and self._plugins[dir_name].is_loaded:
            return True
        
        spec = spec_from_file_location(self.get_plugin_full_name(dir_name), str(self.plugin_dir / dir_name / "plugin.py"))
        module = module_from_spec(spec)

        sys.modules[module.__name__] = module

        if isinstance(plugin, str):
            plugin = PluginInfo(plugin, SemanticVersion(0, 0, 0), "", dir_name)
            self._plugins[dir_name] = Plugin(plugin, None)
        
        try:
            spec.loader.exec_module(module)
        except Exception:
            del sys.modules[module.__name__]
            del self._plugins[dir_name]
            raise

        if isinstance(plugin, str):
            if not hasattr(module, "__version__"):
                return False
            plugin.version = SemanticVersion.parse(module.__version__)
            plugin.description = getattr(module, "__description__", getattr(module, "__doc__", ""))
        if _plugin is None:
            _plugin = Plugin(plugin, None)
        _plugin.module = module
        self._plugins[dir_name] = _plugin

        return True

    def load_plugins(self, dir_names: list[str]):
        for dir_name in dir_names:
            self.load_plugin(dir_name)

    @classmethod
    def get_plugin_full_name(cls, plugin: str | PluginInfo) -> str:
        if isinstance(plugin, PluginInfo):
            plugin = plugin.dir_name
        return f"{cls.PLUGIN_PREFIX}.{plugin}"
