from json import load
from .tree_node import TreeNode
from pathlib import Path

HERE = Path(__file__).parent

def get_tree():
    return TreeNode(load(open(f"{HERE}/default_tree.json", "r")))
