import ez
from ez.events import HTTP
from .html.element import Element
from .components.component import Component
from .events import TreeRenderer
from .renderer import render
from .default_tree import default_tree
from .server import mount


@ez.on(HTTP.GET)
def on_http_get(request):
    def render_tree(response):
        if isinstance(ez.response.body, (Component, Element)):
            ez.emit(TreeRenderer.WillRender, ez.response.body)
            result = render(ez.response.body)
            ez.emit(TreeRenderer.DidRender, ez.response.body, result)
            ez.response.html(result)
            return

    ez.once(HTTP.Out, render_tree)


@ez.get("/")
def index():
    return default_tree()


mount(ez._app)
