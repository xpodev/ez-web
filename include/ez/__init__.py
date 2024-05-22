from typing import TYPE_CHECKING

from .errors import EZError


if TYPE_CHECKING:
    from pathlib import Path

    from . import (
        data,
        database,
        events,
        log,
        lowlevel,
        pages,
        plugins,
        site,
        web,
    )


EZ_FRAMEWORK_VERSION: str
EZ_FRAMEWORK_DIR: "Path"

EZ_PYTHON_EXECUTABLE: str

SITE_DIR: "Path"


del TYPE_CHECKING

__all__ = [
    "EZError",
    "EZ_FRAMEWORK_VERSION",
    "EZ_FRAMEWORK_DIR",
    "EZ_PYTHON_EXECUTABLE",
    "SITE_DIR",

    "data",
    "database",
    "events",
    "log",
    "lowlevel",
    "pages",
    "plugins",
    "site",
    "web",
]
