import ez

from jsx.server import mount
from jsx.renderer import render
from jsx.components import Component
from jsx.html import Element
from ez.events import HTTP, TreeRenderer


@ez.on(HTTP.Out)
def render_tree(_):
    if ez.request.method != "GET":
        return

    if isinstance(ez.response.body, (Component, Element)):
        ez.emit(TreeRenderer.WillRender, ez.response.body)
        result = render(ez.response.body)
        ez.emit(TreeRenderer.DidRender, ez.response.body, result)
        ez.response.html(result)

mount(ez._app)

__title__ = "EZ JSX Integration"
__version__ = "1.0.0"
__description__ = \
"""
This module enables the jsx library for use in EZ Web Framework.
"""
