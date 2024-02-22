import ez

from jsx.server import JSXServer
from jsx.renderer import render
from jsx.components import Component
from jsx.html import Element
from ez.events import HTTP
from .events import TreeRenderer
from . import components


jsx_server = JSXServer()


@ez.on(HTTP.Out)
def render_tree(_):
    if ez.request.method != "GET":
        return

    body = ez.response.body
    if isinstance(body, (Component, Element)):
        if not isinstance(body, components.Page):
            body = components.Page(body)

        ez.emit(TreeRenderer.WillRender, body)
        result = render(body)
        ez.emit(TreeRenderer.DidRender, body, result)
        ez.response.html(result)


jsx_server.mount(ez._app)

ez.extend_ez(components, "jsx")

__module_name__ = "EZ JSX Integration"
