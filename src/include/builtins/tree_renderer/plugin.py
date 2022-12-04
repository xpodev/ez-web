# from ez import ez
import ez
from ez.events import HTTP
from .transpiler.compile_tree import compile_tree
from .transpiler.default_tree import get_tree
from .transpiler.tree_node import EzTree
from .events import TreeRenderer


@ez.on(HTTP.GET)
def on_http_get(request):
    tree = get_tree()

    def render_tree(response):
        # Don't render the tree if the response is already set
        if ez.response.body is not None:
            return

        ez_tree = EzTree(tree)
        ez.emit(TreeRenderer.WillRender, ez_tree)
        ez.response.html(compile_tree(tree))
        ez.emit(TreeRenderer.DidRender, ez_tree, ez.response.body)

    ez.once(HTTP.Out, render_tree)
