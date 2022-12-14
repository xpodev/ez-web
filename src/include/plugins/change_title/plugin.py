from ez import ez
from include.builtins.tree_renderer.events import TreeRenderer
from include.builtins.tree_renderer.transpiler.tree_node import EzTree

@ez.on(TreeRenderer.WillRender)
def update_title(tree: EzTree):
    title_tag = tree.look_for_tag("title")[0]
    title_tag.children[0] = "New Title"

