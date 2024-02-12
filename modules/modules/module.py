from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

from utilities.semver import SemanticVersion


@dataclass
class Module:
    name: str
    entry_point: ModuleType
    entry_point_path: Path
    version: SemanticVersion
    description: str

    def __str__(self) -> str:
        return f"{self.name} v{self.version} @ {self.entry_point_path}"
