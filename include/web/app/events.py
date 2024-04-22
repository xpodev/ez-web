from enum import StrEnum


class App(StrEnum):
    DidStart = "App.DidStart"
    """
    Called after the app is started.
    """
    WillStop = "App.WillStop"
    """
    Called before the app is stopped.
    """
    WillReload = "App.WillReload"
    """
    Called before the app is reloaded.
    """
