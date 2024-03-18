from utilities.event import Event


class Plugins(Event):
    WillLoad = "Plugins.WillLoad"
    """
    Called when the builtins plugins are loaded, before the plugins are loaded.

    :param plugin_list: A list of plugins names that will be loaded.
    """

    DidLoad = "Plugins.DidLoad"
    """
    Called after the plugins are loaded.

    :param plugin_list: A list of plugins names that were loaded.
    """

    Enabled = "Plugins.Enabled"
    """
    Called when a plugin is enabled.

    :param plugin_name: The name of the plugin that was enabled.
    """
    Disabled = "Plugins.Disabled"
    """
    Called when a plugin is disabled.

    :param plugin_name: The name of the plugin that was disabled.
    """
    Reloaded = "Plugins.Reloaded"
    """
    Called when a plugin is reloaded.

    :param plugin_name: The name of the plugin that was reloaded.
    """
    Installed = "Plugins.Installed"
    """
    Called when a plugin is installed.

    :param plugin_name: The name of the plugin that was installed.
    """
    Uninstalled = "Plugins.Uninstalled"
    """
    Called when a plugin is uninstalled.

    :param plugin_name: The name of the plugin that was uninstalled.
    """
