import ez
from ez.events import HTTP
from .events import TreeRenderer
from .renderer import render
from .default_tree import default_tree


@ez.on(HTTP.GET)
def on_http_get(request):
    def render_tree(response):
        # Don't render the tree if the response is already set
        if ez.response.body is not None:
            return

        tree = default_tree()
        ez.emit(TreeRenderer.WillRender, tree)
        result = render(tree)
        ez.emit(TreeRenderer.DidRender, tree, result)
        ez.response.html(result)

    ez.once(HTTP.Out, render_tree)
