import ez
from ez.events import HTTP
from .pyx.renderer import render
from .default_tree import default_tree


@ez.on(HTTP.GET)
def on_http_get(request):
    def render_tree(response):
        # Don't render the tree if the response is already set
        if ez.response.body is not None:
            return

        ez.response.html(render(default_tree()))

    ez.once(HTTP.Out, render_tree)
