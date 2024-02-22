import ez

from . import router

del router

from .builtins.dbi import PLUGIN_REPOSITORY
from .manager import PLUGIN_MANAGER
from .ez_plugins.events import Plugins

from ez.database import engine

PLUGIN_REPOSITORY.connect(engine)


def load_plugins():
    plugins = PLUGIN_REPOSITORY.all()
    plugin_ids = [plugin.package_name for plugin in plugins]

    ez.emit(Plugins.WillLoad, plugins)

    PLUGIN_MANAGER.load_plugins(
        *plugin_ids,
        loader=lambda plugin: PLUGIN_REPOSITORY.get(plugin).default_loader_id
    )
    PLUGIN_MANAGER.run_plugins(*plugin_ids)

    ez.emit(Plugins.DidLoad, plugins)


load_plugins()
