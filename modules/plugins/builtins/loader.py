import sys

from types import ModuleType
from importlib.util import spec_from_file_location, module_from_spec

from utilities.version import Version

from ..plugin import Plugin, PluginInfo, PluginId
from ..machinery.loader import IPluginLoader, PluginLoaderInfo

from .plugin import EZPlugin
from .plugin_module_loader import PluginModuleLoader
from .plugin_module import PluginModule


class EZPluginLoader(IPluginLoader):
    info = PluginLoaderInfo(
        id="ez.plugins.loader",
        name="EZ Plugin Loader",
    )

    EZ_PLUGIN_ENTRY_POINT_FILENAME = "plugin.py"
    EZ_PLUGIN_API_ATTRIBUTE_NAME = "__api__"
    EZ_PLUGIN_INFO_ATTRIBUTE_NAME = "__info__"
    EZ_PLUGIN_MAIN_FUNCTION_NAME = "main"
    EZ_PLUGIN_PREFIX = "ez.current-site.plugins"

    def __init__(self, plugin_dir: PluginId) -> None:
        super().__init__(plugin_dir)

        self._loader = PluginModuleLoader()

        root = sys.modules[self.EZ_PLUGIN_PREFIX] = PluginModule(self.EZ_PLUGIN_PREFIX)
        root.__path__ = [str(self.plugin_dir)]

    def load(self, plugin_id: PluginId, plugin: Plugin) -> EZPlugin | None:
        if plugin is None:
            return self._load_plugin(plugin_id)
        plugin = self._assert_ez_plugin(plugin)
        if plugin.is_loaded:
            if plugin.enabled:
                return None
            self._reload_plugin(plugin)
        else:
            plugin.module = self._load_module(plugin.info.package_name)

    def _load_plugin(self, plugin_id: PluginId) -> EZPlugin:
        module = self._load_module(plugin_id)
        sys.modules[module.__name__] = module

        plugin_dir = self.plugin_dir / plugin_id

        with open(plugin_dir / "plugin-metadata") as file:
            metadata = {
                    key.strip(): value.strip()
                    for key, value in (line.split(":", 1) for line in file)
                }
            metadata["version"] = Version.parse(metadata["version"])
            if "description" not in metadata:
                metadata["description"] = module.__doc__
            info = PluginInfo.model_construct(
                **metadata
            )

        module.__info__ = info
        module.__loader__ = self.info.id
        module.__path__.append(str(plugin_dir))

        ez_plugin = EZPlugin(
            info=info,
            loader=self.info,
            enabled=True,
            api=None,
            module=module
        )

        module.__plugin__ = ez_plugin

        self._execute_module(module)

        ez_plugin.api = getattr(module, self.get_api_attribute_name(), None)

        return ez_plugin
    
    def run_main(self, plugin: Plugin) -> None:
        plugin = self._assert_ez_plugin(plugin)
        if plugin.enabled:
            main = getattr(plugin.module, self.EZ_PLUGIN_MAIN_FUNCTION_NAME, None)
            if callable(main):
                main()

    def _load_module(self, plugin_id: PluginId) -> PluginModule:
        path = self._get_plugin_path(plugin_id)
        spec = spec_from_file_location(self.get_module_full_name(plugin_id), str(path), loader=self._loader)
        module = module_from_spec(spec)
        return module
    
    def _execute_module(self, module: ModuleType) -> None:
        module.__spec__.loader.exec_module(module)

    def _reload_plugin(self, plugin: EZPlugin) -> None:
        self._execute_module(plugin.module)

    def _get_plugin_path(self, plugin_id: PluginId):
        return self.plugin_dir / str(plugin_id) / self.get_entry_point_filename()
    
    def _assert_ez_plugin(self, plugin: Plugin) -> EZPlugin:
        if not isinstance(plugin, EZPlugin):
            raise TypeError(f"Expected EZPlugin, got {type(plugin)}")
        return plugin
    
    @classmethod
    def get_entry_point_filename(cls) -> str:
        return cls.EZ_PLUGIN_ENTRY_POINT_FILENAME
    
    @classmethod
    def get_api_attribute_name(cls) -> str:
        return cls.EZ_PLUGIN_API_ATTRIBUTE_NAME
    
    @classmethod
    def get_info_attribute_name(cls) -> str:
        return cls.EZ_PLUGIN_INFO_ATTRIBUTE_NAME
    
    @classmethod
    def get_module_full_name(cls, plugin_id: PluginId) -> str:
        return f"{cls.EZ_PLUGIN_PREFIX}.{plugin_id}"
