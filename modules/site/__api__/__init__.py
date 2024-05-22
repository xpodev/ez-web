import ez

from ..config import config
from .. import typing as check

DIR = ez.SITE_DIR
CONFIG = config

if check.is_v1(config):
    PLUGINS = DIR / config.overwrites.plugin_directory
    TEMPLATES = DIR / config.overwrites.template_directory
    STATIC = DIR / config.overwrites.static_directory
    RESOURCES = DIR / config.overwrites.resource_directory

    API_URL = config.overwrites.api_url
    SITE_URL = config.overwrites.site_url
else:
    from . import constants as cs

    PLUGINS = DIR / cs.PLUGIN_DIR
    TEMPLATES = DIR / cs.TEMPLATE_DIR
    STATIC = DIR / cs.STATIC_DIR
    RESOURCES = DIR / cs.RESOURCE_DIR

    API_URL = cs.API_URL
    SITE_URL = cs.SITE_URL

del check
del ez
del config


__all__ = [
    "DIR",
    "CONFIG",
    
    "PLUGINS",
    "TEMPLATES",
    "STATIC",
    "RESOURCES",

    "API_URL",
    "SITE_URL"
]
