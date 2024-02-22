from ..manager import TEMPLATE_MANAGER
from ..template import template


def get_template_manager():
    return TEMPLATE_MANAGER


__all__ = [
    "get_template_manager",
    "template",
]
