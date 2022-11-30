from ez import Ez
from include.builtins.tree_renderer.events import TreeRenderer

def update_title():
    title_tag = Ez.tree.look_for_tag("title")[0]
    title_tag.children[0] = "New Title"


@Ez.on(TreeRenderer.WillRender)
def on_incoming_request(response):
    update_title()
