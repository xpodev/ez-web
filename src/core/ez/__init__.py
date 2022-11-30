from typing import Callable
from fastapi import Request
from pyee import EventEmitter

from core.default_tree import get_tree
from core.tree_node import EzTree
from core.ez.response import response


class _Ez(EventEmitter):
    def __init__(self):
        super().__init__()
        self.response = response
        self.request: Request = None
        self.tree = EzTree(get_tree())

    def _add_event_handler(self, event: str, k: Callable, v: Callable):
        current_plugin = _Ez.__INTERNAL_VARIABLE_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__.current_plugin

        def on_deactivate(plugin: str):
            if plugin == current_plugin:
                self.remove_listener(event, k)
                self.remove_listener("plugins.deactivate", on_deactivate)

        super()._add_event_handler("plugins.deactivate", on_deactivate, on_deactivate)

        return super()._add_event_handler(event, k, v)

    def reload_tree(self):
        self.tree = EzTree(get_tree())

    class __INTERNAL_VARIABLE_DO_NOT_TOUCH_OR_YOU_WILL_BE_FIRED__:
        current_plugin: str = None


Ez = _Ez()
