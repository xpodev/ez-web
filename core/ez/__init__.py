from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
del load_dotenv


from args import args, unparsed_args


from pathlib import Path
from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable

from fastapi import FastAPI, Request


# region Variables


response: "_EzResponse | None" = None
request: "Request | None" = None

SITE_DIR: Path = args.sitedir.resolve()
EZ_FRAMEWORK_DIR: Path = Path(__file__).parents[2]
PLUGINS_DIR: Path = SITE_DIR / "plugins"
MODULE_DIR: Path = EZ_FRAMEWORK_DIR / "modules"
PLUGIN_API_DIR: Path = SITE_DIR / "lib" / "public-api" / "plugins"
EZ_ROUTE_ATTRIBUTE = "ez_web_route"

# endregion


# region Load Modules


import sys

sys.path.append(str(MODULE_DIR))

import log

from modules.manager import ModuleManager
from utilities.event import Event
from utilities.event_emitter import EventEmitter
from web.response import _EzResponse
from web.app.app import EZApplication

from ez.errors import EZError

sys.path.remove(str(MODULE_DIR))

# endregion


# region EZ Internal


__path__ = list(__path__)


class _EZ:
    ez: "_EZ | None" = None
    ee: EventEmitter
    app: FastAPI

    plugin_events: dict[str, list[tuple[str, Callable]]]
    currently_loaded_plugin: str | None

    mm: ModuleManager

    def __init__(
        self, app: FastAPI | None = None, ee: EventEmitter | None = None
    ) -> None:
        if _EZ.ez is not None:
            raise RuntimeError("An instance of _EZ already exists.")
        _EZ.ez = self

        self.ee = ee or EventEmitter()
        self.app = app or EZApplication(redirect_slashes=True)

        self.plugin_events = {}

        self.mm = ModuleManager(MODULE_DIR)

    def add_plugin_event(self, plugin: str, event: str, handler: Callable):
        if plugin not in self.plugin_events:
            self.plugin_events[plugin] = []
        self.plugin_events[plugin].append((event, handler))

    def remove_plugin_events(self, plugin: str):
        if plugin in self.plugin_events:
            for event, handler in self.plugin_events[plugin]:
                self.ee._remove_event_listener(event, handler)
            del self.plugin_events[plugin]

    def get_plugin_from_handler(self, handler: Callable, __Path=Path) -> str:
        PLUGIN_PREFIX = "ez.current-site.plugins"
        if not handler.__module__.startswith(PLUGIN_PREFIX):
            return None
        name = handler.__module__.removeprefix(PLUGIN_PREFIX + ".").split(".")[0]
        return name

    def can_register_events(self):
        return (
            not hasattr(self, "currently_loaded_plugin")
            or self.currently_loaded_plugin is not None
        )
    
    def assert_can_register_events(self) -> str | None:
        if not self.can_register_events():
            raise RuntimeError(
                "Cannot register events outside of a plugin's load or unload event."
            )
        if getattr(self, "currently_loaded_plugin", None) is None:
            return None
        return self.currently_loaded_plugin


_EZ()


def event_function(f: Callable, *, __wraps=wraps, __ez=_EZ.ez):
    import ez.plugins
    from ez.plugins import UnknownPluginError

    plugin = __ez.get_plugin_from_handler(f)
    if not plugin:
        return f
    try:
        plugin = ez.plugins.get_plugin(plugin)
    except UnknownPluginError:
        return f
    else:

        @__wraps(f)
        def wrapper(*args, **kwargs):
            if plugin.enabled:
                return f(*args, **kwargs)
            return

        f.__ez_plugin__ = wrapper.__ez_plugin__ = plugin
        return wrapper


def is_plugin_event_handler(f):
    return callable(f) and getattr(f, "__ez_plugin__", None) is not None


def extend_ez(module, alias: str = None, *, THIS=sys.modules[__name__]):
    import sys
    from pathlib import Path

    path = Path(module.__file__)

    name = alias or path.stem
    setattr(THIS, alias or path.stem, module)
    sys.modules[f"ez.{name}"] = module


# endregion


# region Event System


def on(event: Event, maybe_f: Callable = None, *, priority: int = 0, __ez=_EZ.ez):
    """
    Adds a listener to an event.

    :param event: The event to listen to.
    :param priority: The priority of the listener.
    """

    def _on(f):
        plugin = __ez.assert_can_register_events()
        if plugin:
            __ez.add_plugin_event(plugin, event, f)
        
        return __ez.ee.on(event, f, f, priority)

    if maybe_f is not None:
        return _on(maybe_f)
    return _on


def once(event: Event, maybe_f: Callable = None, *, priority: int = 0, __ez=_EZ.ez):
    """
    Adds a listener to an event that will only be called once.

    :param event: The event to listen to.
    :param priority: The priority of the listener.
    """

    def _once(f):
        plugin = __ez.assert_can_register_events()
        if plugin:
            __ez.add_plugin_event(plugin, event, f)
        return __ez.ee.once(event, f, priority)

    if maybe_f is not None:
        return _once(maybe_f)
    return _once


def emit(event: Event, *args, __ez=_EZ.ez, **kwargs):
    """
    Emits an event.

    :param event: The event to emit.
    """
    return __ez.ee.emit(event, *args, **kwargs)


# endregion


# region Module System


def reload_modules(__ez=_EZ.ez):
    return __ez.mm.load_modules(reload=True)


def get_modules(__ez=_EZ.ez):
    return __ez.mm.get_modules()


# endregion


# region Routing


def add_route(
    route: str,
    methods: list[str],
    __ez=_EZ.ez,
    __wraps=wraps,
    __iscoroutinefunction=iscoroutinefunction,
) -> Callable[[Callable], None]:
    """
    Adds a route to the FastAPI app.

    :param route: The route to add.
    :param methods: The methods to allow.
    """

    def decorator(handler):
        handler = event_function(handler)

        if __iscoroutinefunction(handler):

            @__wraps(handler)
            async def wrapper(*args, **kwargs):
                result = await handler(*args, **kwargs)
                return response._auto_body(result)

            setattr(wrapper, EZ_ROUTE_ATTRIBUTE, True)
            __ez.app.add_api_route(route, endpoint=wrapper, methods=methods)
        else:

            @__wraps(handler)
            def wrapper(*args, **kwargs):
                result = handler(*args, **kwargs)
                return response._auto_body(result)

            setattr(wrapper, EZ_ROUTE_ATTRIBUTE, True)
            __ez.app.add_api_route(route, endpoint=wrapper, methods=methods)

        log.debug(f"{methods} {route} -> {handler.__name__}")

    return decorator


# region: Methods


def get(route: str, __ez=_EZ.ez):
    """
    Adds a GET route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["GET"])


def post(route: str):
    """
    Adds a POST route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["POST"])


def put(route: str):
    """
    Adds a PUT route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["PUT"])


def delete(route: str):
    """
    Adds a DELETE route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["DELETE"])


def patch(route: str):
    """
    Adds a PATCH route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["PATCH"])


def options(route: str):
    """
    Adds a OPTIONS route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["OPTIONS"])


def head(route: str):
    """
    Adds a HEAD route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["HEAD"])


def trace(route: str):
    """
    Adds a TRACE route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["TRACE"])


def connect(route: str):
    """
    Adds a CONNECT route to the FastAPI app.

    :param route: The route to add.
    """
    return add_route(route, ["CONNECT"])


def all(route: str):
    """
    Adds a route to the FastAPI app that accepts any HTTP method.

    :param route: The route to add.
    """
    return add_route(
        route,
        [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "OPTIONS",
            "HEAD",
            "TRACE",
            "CONNECT",
        ],
    )


# endregion


# endregion


def _setup(__ez=_EZ.ez):
    if hasattr(__ez.app, "setup"):
        __ez.app.setup()

    from ez.events import Modules

    emit(Modules.WillLoad)
    if not __ez.mm.load_modules(reload=False):
        log.info("No modules were loaded.")
    else:
        log.info(f"Loaded {len(get_modules())} modules from '{MODULE_DIR}'")
    emit(Modules.DidLoad)

    del Modules

    from ez.plugins import PluginEvent, __pm

    plugins = ["test-plugin", "title-changer"]
    emit(PluginEvent.WillLoad, plugins)

    for plugin_id in __pm.load_plugins(*plugins):
        __ez.currently_loaded_plugin = plugin_id
    for plugin in __pm.run_plugins(*plugins):
        __ez.currently_loaded_plugin = plugin.info.package_name

    emit(PluginEvent.DidLoad, plugins)

    del PluginEvent


def _run(setup=_setup):
    setup()


def run(_run=_run):
    """
    Run the EZ Web Server.
    """
    return _run()


_app = _EZ.ez.app


# region: Cleanup


del EventEmitter
del Event
del _EZ

del EZApplication
# del PluginManager
del ModuleManager

# del UnknownPluginError

del FastAPI

del _run
del _setup

del _EzResponse
del wraps
del iscoroutinefunction
del Callable

del Path

del sys

__all__ = [
    "EZError",
    "on",
    "once",
    "emit",
    "run",
]


# endregion
