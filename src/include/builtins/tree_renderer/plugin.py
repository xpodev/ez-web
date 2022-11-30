from ez import Ez
from ez.builtins_events import HTTP
from .lib.compile_tree import compile_tree
from .lib.default_tree import get_tree
from .lib.tree_node import EzTree
from .events import TreeRenderer

@Ez.on(HTTP.In)
def on_http_in(request):
    tree = get_tree()
    setattr(Ez, "tree", EzTree(tree))


@Ez.on(HTTP.Out)
def on_http_out(response):
    Ez.emit(TreeRenderer.WillRender, Ez.tree)
    Ez.response.html(compile_tree(Ez.tree.tree))
    Ez.emit(TreeRenderer.DidRender, Ez.tree, Ez.response.body)
