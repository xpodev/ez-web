from typing import Any, Dict, List, Optional


class TreeNode:
    def __init__(self, tree) -> None:
        self.tag = tree["tag"]
        self.props = tree["props"]
        self.children = tree["children"]

        if self.children is None:
            return

        for i, child in enumerate(self.children):
            if type(child) == dict:
                self.children[i] = TreeNode(child)

    tag: str
    props: Optional[Dict[str, Any]]
    children: Optional[List["TreeNode"]]


class EzTree:
    def __init__(self, tree: TreeNode) -> None:
        self.tree = tree

    def look_for_tag(self, tag: str):
        return self._look_for_tag(self.tree, tag)

    def _look_for_tag(self, tree: TreeNode, tag: str):
        found: List[TreeNode] = []
        if tree.tag == tag:
            found.append(tree)

        if tree.children is None:
            return found

        for child in tree.children:
            if type(child) != TreeNode:
                continue

            found += self._look_for_tag(child, tag)

        return found
