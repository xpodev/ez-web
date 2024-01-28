from fastapi import Request

from ez.html.components import Page
from ..pyx.components.plugin_list import PluginList
from include.plugins_loader import enable_plugin, disable_plugin

import ez


class Plugin:
    def __init__(self, name: str, description: str, version: str, author: str):
        self.name = name
        self.description = description
        self.version = version
        self.author = author


plugins = [
    Plugin(
        "DatabaseConnector", "Connects to various databases", "1.2.2", "TechConnect"
    ),
    Plugin("ImageProcessor", "Processes and edits images", "2.0.3", "MediaMagic"),
    Plugin(
        "AuthenticationModule", "Handles user authentication", "1.5.77", "SecureAuth"
    ),
    Plugin(
        "DataAnalyticsTool", "Provides insights from data", "3.1.5a", "InsightfulTech"
    ),
    Plugin(
        "NotificationService", "Sends notifications to users", "2.5.7rc2", "NotifyMe"
    ),
]


def activate(plugin_name: str):
    enable_plugin(plugin_name)


def deactivate(plugin_name: str):
    disable_plugin(plugin_name)


@ez.get("/plugins")
def plugin_list():
    return Page(PluginList(plugins))


@ez.post("/api/plugins/activate")
def on_activate(request: Request):
    plugin_name = request.query_params.get("plugin")
    activate(plugin_name)


@ez.post("/api/plugins/deactivate")
def on_deactivate(request: Request):
    plugin_name = request.query_params.get("plugin")
    deactivate(plugin_name)
