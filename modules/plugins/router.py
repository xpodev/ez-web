import ez
import ez.plugins


@ez.get("/api/plugins")
def get_plugins():
    return [plugin.info.model_dump() for plugin in ez.plugins.get_plugins()]


@ez.post("/api/plugins/{plugin_id}/enable")
def enable_plugin(plugin_id: str):
    print(f"Enabling plugin {plugin_id}...")
    ez.plugins.enable_plugin(plugin_id)
    return "Plugin enabled!"


@ez.post("/api/plugins/{plugin_id}/disable")
def disable_plugin(plugin_id: str):
    print(f"Disabling plugin {plugin_id}...")
    ez.plugins.disable_plugin(plugin_id)
    return "Plugin disabled!"
