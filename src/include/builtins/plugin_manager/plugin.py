from fastapi import Request
from ez import Ez
from include.plugins_loader import activate_plugin, deactivate_plugin


def activate(plugin_name: str):
    activate_plugin(plugin_name)


def deactivate(plugin_name: str):
    deactivate_plugin(plugin_name)


def on_activate(request: Request):
    plugin_name = request.query_params.get("plugin")
    activate(plugin_name)


def on_deactivate(request: Request):
    plugin_name = request.query_params.get("plugin")
    deactivate(plugin_name)


Ez.add_route("/activate", on_activate)
Ez.add_route("/deactivate", on_deactivate)
