import warnings


def current_application():
    from .host import AppHost

    return AppHost.current_host.current_application


def current_plugin():
    warnings.warn("This function should not be used yet because the plugin host was not yet refactored")

    return current_application()
