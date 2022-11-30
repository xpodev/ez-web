from json import load
from core.tree_node import TreeNode


def get_tree():
    return TreeNode(load(open("src/core/default_tree.json", "r")))
