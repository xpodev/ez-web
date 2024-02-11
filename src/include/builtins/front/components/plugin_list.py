from .plugin_info import PluginInfo
from ez.pyx import Div, Component


class PluginList(Component):
    def __init__(self, plugins):
        self.plugin_list = plugins

    def render(self):
        return Div(
            *[PluginInfo(plugin) for plugin in self.plugin_list],
            class_name="w-25 mx-auto bg-light p-3",
        )