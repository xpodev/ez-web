import dis
from ez.database.models.plugin import Plugin
from ez.html import Small, H3, Div
from ez.html.components import Component
from ...pyx.html.input import Input


class PluginInfo(Component):
    def __init__(self, plugin: Plugin):
        self.plugin = plugin

    def render(self):
        return Div(
            H3(self.plugin.name),
            Div(self.plugin.description),
            Div(
                Small(f"Version: {self.plugin.version}"),
                Small(f"Author: {self.plugin.author}"),
                style="display: flex; justify-content: space-between;",
            ),
            Div(
                Input(
                    type="checkbox",
                    checked=self.plugin.enabled,
                    disabled=True,
                )
            ),
            class_name="plugin-info",
        )
