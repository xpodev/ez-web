import ez

import ez.log

ez.log.info("Plugin Manager loaded")


from .builtins.dbi import PLUGIN_REPOSITORY
from ez.plugins.events import Plugins

from ez.database import engine

PLUGIN_REPOSITORY.connect(engine)

from .manager import PLUGIN_MANAGER


def load_plugins():
    plugins = PLUGIN_REPOSITORY.all()
    plugin_ids = [plugin.package_name for plugin in plugins]

    plugin_ids = [
        "title-changer",
        "test-plugin",
    ]

    ez.events.emit(Plugins.WillLoad, plugins)

    PLUGIN_MANAGER.load_plugins(
        *plugin_ids,
        loader=lambda plugin: None# PLUGIN_REPOSITORY.get(plugin).default_loader_id
    )
    PLUGIN_MANAGER.run_plugins(*plugin_ids)

    ez.events.emit(Plugins.DidLoad, plugins)


load_plugins()
PLUGIN_MANAGER.enable_public_api()
