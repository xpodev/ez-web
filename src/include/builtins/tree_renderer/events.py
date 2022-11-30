from enum import Enum

class TreeRenderer(Enum):
    WillRender = "TreeRenderer.WillRender"
    """
    Called before the tree is rendered.
    
    :param EzTree tree: The tree that will be rendered.
    """

    DidRender = "TreeRenderer.DidRender"
    """
    Called after the tree is rendered.

    :param EzTree tree: The tree that was rendered.
    :param str html: The HTML that was rendered.
    """
