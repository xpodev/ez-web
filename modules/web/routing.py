from typing import cast

import ez

from starlette.routing import BaseRoute, Router, Mount

from sandbox.applications import Application, Artifact
from sandbox.host import AppHost

from .router import EZRouter


class PluginRouter:
    _mounts: dict[Application, Mount]

    def __init__(self) -> None:
        self._router = Router()
        self._mounts = {}

    @property
    def router(self):
        return self._router
    
    def add_router(self, app: Application, route: str, *, cls: type[Router] = EZRouter) -> Router:
        if app in self._mounts:
            return cast(Router, self._mounts[app].app)
        
        router = cls()
        mount = Mount(route, app=router)

        if not app.is_root:
            self._mounts[app] = mount

            def _on_disable():
                if app not in self._mounts:
                    return
                
                router = self._mounts.pop(app)
                try:
                    self._router.routes.remove(router)
                except ValueError:
                    ...

            AppHost.current_host.create_artifact(app, Artifact, _on_disable)

        self._router.mount(route, router)

        return router
    
    def get_router(self, app: Application) -> Router | None:
        try:
            return cast(Router, self._mounts[app].app)
        except KeyError:
            return None


MAIN_ROUTER = ez.lowlevel.WEB_APP.router

API_URL = ez.site.API_URL
API_ROUTER = PluginRouter()
API_MOUNT = Mount(API_URL, app=API_ROUTER.router)


def add_route(route: BaseRoute):
    MAIN_ROUTER.routes.append(route)


def mount(route: str, router: Router, **kwargs):
    MAIN_ROUTER.mount(route, router, **kwargs)
