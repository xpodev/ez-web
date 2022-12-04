import sys
import re
from importlib import import_module, reload
# from ez import ez
import ez
from ez.events import Plugins
from pathlib import Path


# This is mocking a database
enabled_plugins = set()

_PLUGIN_ENTRY_POINT = "plugin"
HERE = Path(__file__).parent


def _import_plugin(plugin_dir: str):
    ez.__INTERNAL_VARIABLES_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.currently_loaded_plugin = plugin_dir.split(
        "/")[-1]

    plugin_path = Path(f"{HERE}/{plugin_dir}/{_PLUGIN_ENTRY_POINT}.py")
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
            print(f"Failed to load builtin plugin {plugin.name}")

    ez.emit(Plugins.WillLoad, enabled_plugins)

    for plugin in enabled_plugins:
        _import_plugin(f"plugins.{plugin}")

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
