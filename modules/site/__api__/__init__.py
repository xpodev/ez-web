import ez

from ..config import config

DIR = ez.SITE_DIR
CONFIG = config


del ez
del config


__all__ = ["DIR", "CONFIG"]
