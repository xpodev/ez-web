from fastapi import Request
from ez import Ez
from include.plugins_loader import enable_plugin, disable_plugin


def activate(plugin_name: str):
    enable_plugin(plugin_name)


def deactivate(plugin_name: str):
    disable_plugin(plugin_name)


@Ez.post("/api/plugins/activate")
def on_activate(request: Request):
    plugin_name = request.query_params.get("plugin")
    activate(plugin_name)


@Ez.post("/api/plugins/deactivate")
def on_deactivate(request: Request):
    plugin_name = request.query_params.get("plugin")
    deactivate(plugin_name)
