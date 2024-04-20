from typing import TYPE_CHECKING, Callable


if TYPE_CHECKING:
    from .application import Application


class ArtifactBase:
    _source: "Application"

    def __init__(self, app: "Application") -> None:
        self._source = app

    def __init_subclass__(cls, *args, **kwargs) -> None:
        super().__init_subclass__(*args, **kwargs)

        original_init = cls.__init__

        def __init__(self, app: "Application", *args, **kwargs):
            ArtifactBase.__init__(self, app)

            original_init(self, *args, **kwargs)

        cls.__init__ = __init__

    @property
    def source(self) -> "Application":
        return self._source

    def remove(self) -> bool:
        raise NotImplementedError


class Artifact(ArtifactBase):
    if TYPE_CHECKING:
        def __init__(self, app: "Application", remove: Callable[[], bool | None]) -> None:
            raise NotImplementedError
    else:
        def __init__(self, remove: Callable[[], bool | None]) -> None:
            self._remove = remove

    def remove(self) -> bool:
        return self._remove() is not False
