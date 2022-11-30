from fastapi import Request
from core.ez import Ez
from include.plugin_loader import activate_plugin, deactivate_plugin


def activate(plugin_name: str):
    activate_plugin(plugin_name)


def deactivate(plugin_name: str):
    deactivate_plugin(plugin_name)


@Ez.on("GET[/activate]")
def on_activate(request: Request):
    plugin_name = request.query_params.get("plugin")
    activate(plugin_name)


@Ez.on("GET[/deactivate]")
def on_deactivate(request: Request):
    plugin_name = request.query_params.get("plugin")
    deactivate(plugin_name)
