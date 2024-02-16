from ez.errors import EZError


class EZPluginManagerError(EZError):
    ...


class UnknownPluginError(EZPluginManagerError):
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

    def __str__(self):
        return f"Unknown plugin: {self.plugin_name}"


class PluginAlreadyInstalledError(EZPluginManagerError):
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

    def __str__(self):
        return f"Plugin already installed: {self.plugin_name}"
