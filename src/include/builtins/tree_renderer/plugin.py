from ez import Ez
from ez.events import HTTP
from .transpiler.compile_tree import compile_tree
from .transpiler.default_tree import get_tree
from .transpiler.tree_node import EzTree
from .events import TreeRenderer


@Ez.on(HTTP.GET)
def on_http_get(request):
    tree = get_tree()

    def render_tree(response):
        # Don't render the tree if the response is already set
        if Ez.response.body is not None:
            return

        ez_tree = EzTree(tree)
        Ez.emit(TreeRenderer.WillRender, ez_tree)
        Ez.response.html(compile_tree(tree))
        Ez.emit(TreeRenderer.DidRender, ez_tree, Ez.response.body)

    Ez.once(HTTP.Out, render_tree)
