from typing import TypeGuard, TYPE_CHECKING

if TYPE_CHECKING:
    from .configs.base import BaseSiteConfig

    from .configs.v1 import SiteConfig as SiteConfigV1


def is_v1(config: "BaseSiteConfig") -> TypeGuard["SiteConfigV1"]:
    return config.version == 1
