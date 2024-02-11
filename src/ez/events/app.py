from .event import Event


class App(Event):
    WillStart = "App.WillStart"
    """
    Called before the app is started.
    """
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
