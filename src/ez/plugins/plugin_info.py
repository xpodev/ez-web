from dataclasses import dataclass
from utilities.semver import SemanticVersion


@dataclass
class PluginInfo:
    name: str
    version: SemanticVersion
    description: str
    dir_name: str
