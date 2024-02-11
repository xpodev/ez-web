from .event import Event

class Settings(Event):
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
