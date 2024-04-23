import ez
import ez.lowlevel

from jsx.middlewares import ASGIMiddleware
from jsx.renderer import render
from jsx.components import Component
from jsx.html import Element
from ez.web.http import HTTPEvent
from .events import TreeRenderer


@ez.events.on(HTTPEvent.Out)
def render_tree(_):
    if ez.request.method != "GET":
        return

    body = ez.response.body
    if isinstance(body, (Component, Element)):
        if not isinstance(body, components.Page):
            body = components.Page(body)

        ez.events.emit(TreeRenderer.WillRender, body)
        result = render(body)
        ez.events.emit(TreeRenderer.DidRender, body, result)
        ez.response.html(result)


ez.lowlevel.WEB_APP.add_middleware(ASGIMiddleware)

__module_name__ = "EZ JSX Integration"
