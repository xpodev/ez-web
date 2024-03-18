from .base import BaseSiteConfig
from .v1 import SiteConfig as V1


_Configs = {
    1: V1,
}


def get_config_class(version: int) -> type[BaseSiteConfig]:
    return _Configs[version]


def is_version_supported(version: int) -> bool:
    return version in _Configs
