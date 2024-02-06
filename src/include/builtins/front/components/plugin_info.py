from ez.database.models.plugin import PluginModel
from ez.html import Small, H3, Div, Input
from ez.html.components import Component
from ez.html.style import Style


class PluginInfo(Component):
    def __init__(self, plugin: PluginModel):
        self.plugin = plugin

    def render(self):
        return Div(
            H3(self.plugin.name),
            Div(self.plugin.description),
            Div(
                Small(f"Version: {self.plugin.version}"),
                Small(f"Author: {self.plugin.author}"),
                style=Style(
                    {
                        "display": "flex",
                        "justify-content": "space-between",
                    }
                )
            ),
            Div(
                "Enabled" if self.plugin.enabled else "Disabled",
            ),
            class_name="plugin-info",
        )
