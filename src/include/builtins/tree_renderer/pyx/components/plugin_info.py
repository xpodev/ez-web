from ..html.small import Small
from ..html.h3 import H3
from ..html import Div
from .component import Component


class PluginInfo(Component):
    def __init__(self, plugin):
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
            class_name="plugin-info",
        )
