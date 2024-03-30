from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .application import Application


class ArtifactBase:
    _source: "Application"

    def __init__(self, source: "Application") -> None:
        self._source = source

    @property
    def source(self) -> "Application":
        return self._source

    def remove(self) -> bool:
        raise NotImplementedError
