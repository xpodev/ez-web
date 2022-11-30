from enum import Enum


class Plugins(Enum):
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


class Settings(Enum):
    WillLoad = "Settings.WillLoad"
    """
    Called before the settings are loaded.
    """
    DidLoad = "Settings.DidLoad"
    """
    Called after the settings are loaded.
    """

    WillSave = "Settings.WillSave"
    """
    Called before the settings are saved.
    """
    DidSave = "Settings.DidSave"
    """
    Called after the settings are saved.
    """

    WillReset = "Settings.WillReset"
    """
    Called before the settings are reset.
    """
    DidReset = "Settings.DidReset"
    """
    Called after the settings are reset.
    """

    WillChange = "Settings.WillChange"
    """
    Called before a setting is changed.

    :param setting_name: The name of the setting that is about to be changed.
    :param setting_value: The value of the setting that is about to be changed.
    """
    DidChange = "Settings.DidChange"
    """
    Called after a setting is changed.

    :param setting_name: The name of the setting that was changed.
    :param setting_value: The new value of the setting that was changed.
    """


class HTTP(Enum):
    In = "HTTP.In"
    """
    Called when a HTTP request is received.

    :param request: The request object.
    """
    Out = "HTTP.Out"
    """
    Called when a HTTP response is sent.

    :param request: The request object.
    """

    GET = "HTTP.GET"
    """
    Called when a HTTP GET request is received.

    :param request: The request object.
    """
    POST = "HTTP.POST"
    """
    Called when a HTTP POST request is received.

    :param request: The request object.
    """
    PUT = "HTTP.PUT"
    """
    Called when a HTTP PUT request is received.

    :param request: The request object.
    """
    DELETE = "HTTP.DELETE"
    """
    Called when a HTTP DELETE request is received.

    :param request: The request object.
    """
    PATCH = "HTTP.PATCH"
    """
    Called when a HTTP PATCH request is received.

    :param request: The request object.
    """
    HEAD = "HTTP.HEAD"
    """
    Called when a HTTP HEAD request is received.

    :param request: The request object.
    """
    OPTIONS = "HTTP.OPTIONS"
    """
    Called when a HTTP OPTIONS request is received.

    :param request: The request object.
    """
