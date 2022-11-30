import sys
import re
from importlib import import_module, reload
from core.ez import Ez
from pathlib import Path

# This is mocking a database
enabled_plugins = set()

_PLUGIN_ENTRY_POINT = "plugin"
HERE = Path(__file__).parent

def _import_plugin(plugin_dir: str):
    Ez.__INTERNAL_VARIABLE_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.current_plugin = plugin_dir.split("/")[-1]

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
    for plugin in Path(f"{HERE}/builtins").iterdir():
        if not plugin.is_dir():
            continue

        if not _import_plugin(f"builtins/{plugin.name}"):
            print(f"Failed to load builtin plugin {plugin.name}")

    for plugin in enabled_plugins:
        _import_plugin(f"plugins.{plugin}")



def activate_plugin(plugin: str):
    if plugin not in enabled_plugins:
        _import_plugin(f"plugins/{plugin}")
        Ez.emit("plugins.activate", plugin)
        enabled_plugins.add(plugin)


def deactivate_plugin(plugin: str):
    if plugin in enabled_plugins:
        Ez.emit("plugins.deactivate", plugin)
        enabled_plugins.remove(plugin)