class UnknownPluginError(Exception):
    def __init__(self, plugin_name):
        self.plugin_name = plugin_name

    def __str__(self):
        return f"Unknown plugin: {self.plugin_name}"
