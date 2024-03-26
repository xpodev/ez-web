from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from sandbox.host import AppHost
    from sandbox.applications import Application
    from sandbox.security import Permission


@dataclass
class Module:
    name: str
    entry_point: ModuleType
    entry_point_path: Path
    priority: int = 0

    application_factory: "Callable[[AppHost, str], Application] | None" = None

    def __str__(self) -> str:
        return f"{self.name} @ {self.entry_point_path.parent} ({self.priority})"
    
    def __hash__(self) -> int:
        return hash(self.entry_point_path)
