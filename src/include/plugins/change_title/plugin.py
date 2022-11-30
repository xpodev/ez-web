from ez import Ez
from include.builtins.tree_renderer.events import TreeRenderer
from include.builtins.tree_renderer.lib.tree_node import EzTree

@Ez.on(TreeRenderer.WillRender)
def update_title(tree: EzTree):
    title_tag = tree.look_for_tag("title")[0]
    title_tag.children[0] = "New Title"

