import sys
import re
from importlib import import_module, reload

import ez
from ez.database.models.plugin import PluginModel
from ez.database import select, session
from ez.events import App, Plugins
from pathlib import Path

from ez.log import logger


enabled_plugins = session.scalars(
    select(PluginModel).where(PluginModel.enabled == True)
)

_PLUGIN_ENTRY_POINT = "plugin"
HERE = Path(__file__).parent


def _import_plugin(plugin_dir: str):
    ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.currently_loaded_plugin = plugin_dir.split(
        "/"
    )[
        -1
    ]

    plugin_path = HERE / plugin_dir / f"{_PLUGIN_ENTRY_POINT}.py"
    module_path = re.sub(r"(?:\/|\\)", ".", plugin_dir)
    module_name = f"include.{module_path}.{_PLUGIN_ENTRY_POINT}"

    if not Path(plugin_path).exists():
        return False

    if module_name in sys.modules:
        reload(sys.modules[module_name])
    else:
        import_module(module_name)

    return True


def load_plugins():
    """
    Load all plugins from the plugins directory

    It will also reload the plugins if they are already loaded, which is somewhat
    heavy, so it's best not to use this on every request.

    You probably won't need to call this function ever since it's called
    automatically when the server starts
    """
    for plugin in Path(f"{HERE}/builtins").iterdir():
        if not plugin.is_dir():
            continue

        if not _import_plugin(f"builtins/{plugin.name}"):
            logger.error(f"Failed to load builtin plugin {plugin.name}")

    ez.emit(Plugins.WillLoad, enabled_plugins)

    for plugin in enabled_plugins:
        _import_plugin(f"plugins/{plugin.dir_name}")

    ez.emit(Plugins.DidLoad, enabled_plugins)


def enable_plugin(plugin: str):
    """
    Enable a plugin

    If the plugin is already enabled, this function will do nothing

    :param plugin: The name of the plugin to enable
    """
    if plugin not in enabled_plugins:
        _import_plugin(f"plugins/{plugin}")
        ez.emit(Plugins.Enabled, plugin)
        enabled_plugins.add(plugin)


def disable_plugin(plugin: str):
    """
    Disable a plugin

    If the plugin is already disabled, this function will do nothing

    :param plugin: The name of the plugin to disable
    """
    if plugin in enabled_plugins:
        ez.emit(Plugins.Disabled, plugin)
        enabled_plugins.remove(plugin)


def reload_plugin(plugin: str):
    """
    Reload a plugin

    If the plugin is not enabled, this function will do nothing

    :param plugin: The name of the plugin to reload
    """
    if plugin in enabled_plugins:
        ez.emit(Plugins.Reloaded, plugin)
        _import_plugin(f"plugins/{plugin}")


@ez.get("/api/plugins")
def get_plugins():
    """
    Get the list of all plugins

    :return: The list of all plugins
    """
    return list(repository.active_plugins)


class PluginRepository:
    """
    A repository for the 3rd party plugins
    """

    def __init__(self):
        self.plugins: dict[str, PluginModel] = {}
        self.reload_all()

    def reload_all(self):
        """
        Reload all plugins from the database
        """
        self.plugins = {plugin.dir_name: plugin for plugin in PluginModel.all()}
        for plugin in filter(lambda p: p.enabled, self.plugins.values()):
            self._load(plugin)

    def find(self, name: str):
        """
        Find a plugin by name

        :param name: The unique name of the plugin to find
        :return: The plugin model or None if the plugin was not found
        """
        return self.plugins.get(name, None)

    def _load(self, plugin: PluginModel):
        ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.currently_loaded_plugin = (
            plugin
        )
        module_name = f"include.plugins.{plugin.dir_name}.{_PLUGIN_ENTRY_POINT}"
        if module_name in sys.modules:
            reload(sys.modules[module_name])
        else:
            import_module(module_name)

        plugin.enabled = True
        return True

    def _as_plugin(self, plugin: str | PluginModel):
        if isinstance(plugin, str):
            plugin = self.find(plugin)
        return plugin

    def enable(self, plugin: str | PluginModel):
        """
        Enable a plugin

        If the plugin is already enabled, this function will do nothing

        :param plugin: The name of the plugin to enable
        """
        plugin = self._as_plugin(plugin)
        if not plugin:
            return False

        plugin.enabled = True
        ez.emit(Plugins.Enabled, plugin)
        self._load(plugin)
        return True

    def disable(self, plugin: str | PluginModel):
        """
        Disable a plugin

        If the plugin is already disabled, this function will do nothing

        :param plugin: The name of the plugin to disable
        """
        plugin = self._as_plugin(plugin)
        if not plugin:
            return False

        plugin.enabled = False
        ez.emit(Plugins.Disabled, plugin)
        return True

    def reload(self, plugin: str | PluginModel):
        """
        Reload a plugin

        If the plugin is not enabled, this function will do nothing

        :param plugin: The name of the plugin to reload or the plugin model
        """
        plugin = self._as_plugin(plugin)
        if not plugin or not plugin.enabled:
            return False

        ez.emit(Plugins.Reloaded, plugin)
        self._load(plugin)
        return True

    @property
    def active_plugins(self):
        return list(filter(lambda p: p.enabled, self.plugins.values()))


repository: PluginRepository = None


@ez.on(App.DidStart)
def create_repository():
    global repository

    # load builtins
    for plugin in Path(f"{HERE}/builtins").iterdir():
        if not plugin.is_dir():
            continue

        if not _import_plugin(f"builtins/{plugin.name}"):
            logger.error(f"Failed to load builtin plugin {plugin.name}")

    repository = PluginRepository()
