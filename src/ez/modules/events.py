from ez.events import Event


class Modules(Event):
    WillLoad = "Modules.WillLoad"
    """
    This event is emitted before loading the modules.
    """

    DidLoad = "Modules.DidLoad"
    """
    This event is emitted after loading the modules.
    """
