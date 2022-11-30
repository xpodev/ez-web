from typing import Any, Dict, List, Optional
from core.tree_node import TreeNode


def compile_tree(tree: TreeNode) -> str:
    if type(tree) == str:
        return tree

    if tree.tag == "":
        return _compile_children(tree.children)

    props = _compile_props(tree.props).strip()
    tag = tree.tag
    in_tag = f"{tag} {props}" if props else tag

    if tree.children is None:
        return f"<{in_tag}>"

    return f"""<{in_tag}>{_compile_children(tree.children)}</{tree.tag}>"""


def _compile_props(props: Optional[Dict[str, Any]]) -> str:
    return " ".join([f"{key}={value}" if value != True else f"{key}" for key, value in props.items()])


def _compile_children(children: Optional[List[TreeNode]]) -> str:
    return "".join([compile_tree(child) for child in children])
