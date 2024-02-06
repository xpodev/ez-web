import dis
from ez.database.models.plugin import PluginModel
from ez.pyx import Small, H3, Div, Component, Input


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
