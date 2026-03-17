import ez

import ez.log

ez.log.info("Plugin Manager loaded")


import ez.lowlevel

from .machinery.manager import PluginManager
from .builtins.installer import EZPluginInstaller
from .builtins.loader import EZPluginLoader

from .config import PLUGINS_DIRECTORY, PLUGIN_MANIFEST_FILENAME

from . import manager, router


def init_manager(host):
    manager.PLUGIN_MANAGER = PluginManager(
        host, 
        str(PLUGINS_DIRECTORY), 
        EZPluginInstaller, 
        EZPluginLoader
    )
    return manager.PLUGIN_MANAGER


plugin_manager = init_manager(ez.lowlevel.APP_HOST)


from .builtins.dbi import PLUGIN_REPOSITORY
from .events import Plugins
from .machinery.manifest import PluginManifest

from ez.database import engine


@ez.events.on("App.Started")
def load_plugins():
    PLUGIN_REPOSITORY.connect(engine)
    plugins = PLUGIN_REPOSITORY.all()
    plugin_ids = [plugin.package_name for plugin in plugins]

    for item in plugin_manager.plugin_dir.iterdir():
        if not item.is_dir():
            continue
        if item.name in plugin_ids:
            continue
        
        manifest_file = item / PLUGIN_MANIFEST_FILENAME

        if not manifest_file.exists():
            continue

        manifest = PluginManifest.from_path(manifest_file)

        plugin = PLUGIN_REPOSITORY.create(
            package_name=manifest.package_name,
            name=manifest.name,
            description=manifest.description,
            author=manifest.author,
            version=str(manifest.version),
            home_page=manifest.home_page,
            installer_id=EZPluginInstaller.info.id,
            default_loader_id=EZPluginLoader.info.id
        )

        plugins.append(plugin)
        plugin_ids.append(plugin.package_name)

        PLUGIN_REPOSITORY.set(plugin)

    ez.events.emit(Plugins.WillLoad, plugins)

    plugin_manager.load_plugins(
        *plugin_ids,
        loader=lambda plugin: PLUGIN_REPOSITORY.get(plugin).default_loader_id
    )
    plugin_manager.run_plugins(*plugin_ids)

    plugins = plugin_manager.get_plugins()
    ez.log.info(f"Loaded {len(plugins)} plugins:")
    for plugin in plugins:
        ez.log.info(f"\tLoaded plugin: {plugin.info.package_name}")

    ez.events.emit(Plugins.DidLoad, plugins)


plugin_manager.enable_public_api()
