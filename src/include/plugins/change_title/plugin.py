from core.ez import Ez
from core.tree_node import TreeNode

print("Loaded")

def update_title():
    title_tag = Ez.tree.look_for_tag("title")[0]
    title_tag.children[0] = "New Title"


@Ez.on("compiler.init")
def on_compile_init(tree: TreeNode):
    update_title()
