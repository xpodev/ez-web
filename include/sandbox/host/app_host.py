from contextlib import contextmanager
from typing import Callable, Concatenate, ParamSpec, TypeVar
from sandbox.identity.oid_db import ObjectDatabase
from utilities.singleton import SingletonMeta

from .context import Context
from .security import AppHostPermission

from ..applications import Application, ArtifactBase
from ..security import requires


AppT = TypeVar("AppT", bound=Application)
T = TypeVar("T", bound=ArtifactBase)
P = ParamSpec("P")


class AppHostMeta(SingletonMeta):
    @property
    def current_host(cls) -> "AppHost":
        return cls._instances[cls]


class AppHost(metaclass=AppHostMeta):
    _apps: list[Application]
    _artifacts: dict[Application, list[ArtifactBase]]
    _registered_events: dict[Callable, Application]
    _context: Context
    _db: ObjectDatabase

    def __init__(self, context: Context | Application):
        if isinstance(context, Application):
            context = Context(context)
        self._context = context
        self._root = context.current_application
        self._apps = [self._root]
        self._artifacts = {self._root: []}
        self._registered_events = {}
        self._db = ObjectDatabase()
    
    @property
    def root_application(self):
        return self._root

    @property
    def db(self):
        return self._db

    @property
    def current_application(self):
        return self._context.current_application
    
    @requires(AppHostPermission.ManageApplications)
    def application(self, app: Application):
        return self._context.application(app)

    @requires(AppHostPermission.ManageApplications)
    def add_application(self, app: Application):
        if app._host is not None:
            raise ValueError("Application already has a host")
        app._host = self
        self._apps.append(app)

    @requires(AppHostPermission.CreateApplications)
    def create_application(
            self, 
            app_type: Callable[Concatenate["AppHost", P], AppT],
            *args: P.args,
            **kwargs: P.kwargs
            ) -> AppT:
        app = app_type(self, *args, **kwargs)
        self.add_application(app)
        return app

    @requires(AppHostPermission.ManageApplications)
    def create_artifact(
        self,
        app: Application,
        artifact_factory: Callable[Concatenate["Application", P], T],
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:
        if app not in self._apps:
            raise ValueError("Application not managed by this host")
        if app not in self._artifacts:
            self._artifacts[app] = []
        artifact = artifact_factory(app, *args, **kwargs)
        self._artifacts[app].append(artifact)
        return artifact

    @requires(AppHostPermission.ManageApplications)
    def remove_application(self, app: Application):
        app._host = None
        self.remove_application_artifacts(app)
        self._apps.remove(app)

    @requires(AppHostPermission.ManageApplications)
    def remove_application_artifacts(self, app: Application):
        if app not in self._apps:
            return
        for artifact in self._artifacts.pop(app, ()):
            artifact.remove()

    @requires(AppHostPermission.RegisterEvents)
    def register_event(self, event: Callable):
        self._registered_events[event] = self.current_application

    @requires(AppHostPermission.InvokeEvents)
    def invoke(self, func: Callable, *args, **kwargs):
        try:
            with self._context.application(self._registered_events[func]):
                return func(*args, **kwargs)
        except KeyError:
            return func(*args, **kwargs)