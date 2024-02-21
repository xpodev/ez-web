import ez

from . import router
del router

from .builtins.dbi import PLUGIN_REPOSITORY
from .manager import PLUGIN_MANAGER
from .ez_plugins.events import Plugins

from ez.database import engine

PLUGIN_REPOSITORY.connect(engine)


def load_plugins():
    plugins = [plugin.package_name for plugin in PLUGIN_REPOSITORY.all()]

    ez.emit(Plugins.WillLoad, plugins)

    PLUGIN_MANAGER.load_plugins(*plugins)
    PLUGIN_MANAGER.run_plugins(*plugins)

    ez.emit(Plugins.DidLoad, plugins)


load_plugins()
