"""
Tree Structure Module - TreeNode and BinaryTree classes.
Author: Yair Levi
"""

from typing import Optional, List


class TreeNode:
    """Represents a single node in the binary tree."""

    def __init__(self, name: str, level: int):
        self.name: str = name
        self.level: int = level
        self.token_count: int = 0
        self.left_child: Optional[TreeNode] = None
        self.right_child: Optional[TreeNode] = None
        self.parent: Optional[TreeNode] = None

    def is_leaf(self) -> bool:
        return self.left_child is None and self.right_child is None

    def set_tokens(self, count: int) -> None:
        self.token_count = count

    def calculate_sum(self) -> int:
        """Calculate sum of tokens from children recursively."""
        if self.is_leaf():
            return self.token_count
        left_sum = self.left_child.calculate_sum() if self.left_child else 0
        right_sum = self.right_child.calculate_sum() if self.right_child else 0
        self.token_count = left_sum + right_sum
        return self.token_count

    def __repr__(self) -> str:
        return f"TreeNode({self.name}, level={self.level}, tokens={self.token_count})"


class BinaryTree:
    """Manages the complete binary tree structure."""

    def __init__(self, root: TreeNode, leaves: List[TreeNode]):
        self.root: TreeNode = root
        self.leaves: List[TreeNode] = leaves
        self.all_nodes: List[TreeNode] = []
        self._collect_all_nodes()

    def _collect_all_nodes(self) -> None:
        """Collect all nodes in the tree via traversal."""
        self.all_nodes = []
        self._traverse_collect(self.root)

    def _traverse_collect(self, node: Optional[TreeNode]) -> None:
        if node is None:
            return
        self.all_nodes.append(node)
        self._traverse_collect(node.left_child)
        self._traverse_collect(node.right_child)

    def get_nodes_by_level(self, level: int) -> List[TreeNode]:
        """Get all nodes at a specific level."""
        return [node for node in self.all_nodes if node.level == level]

    def get_all_leaves_sorted(self) -> List[TreeNode]:
        """Get all leaves sorted by name (numerically)."""
        # Sort by numeric part of name (e.g., "1_5" -> 5)
        return sorted(self.leaves, key=lambda n: int(n.name.split('_')[1]))

    def reset_tokens(self) -> None:
        """Reset all token counts to zero."""
        for node in self.all_nodes:
            node.token_count = 0

    def calculate_all_sums(self) -> None:
        """Calculate sums for all nodes from leaves to root."""
        self.root.calculate_sum()


def build_tree() -> BinaryTree:
    """Build a complete binary tree with 5 levels."""
    # Level 1: Create 16 leaves
    leaves = [TreeNode(f"1_{i+1}", level=1) for i in range(16)]

    # Level 2: Create 8 nodes, connect to leaves
    level2 = []
    for i in range(8):
        node = TreeNode(f"2_{i+1}", level=2)
        node.left_child = leaves[i * 2]
        node.right_child = leaves[i * 2 + 1]
        leaves[i * 2].parent = node
        leaves[i * 2 + 1].parent = node
        level2.append(node)

    # Level 3: Create 4 nodes
    level3 = []
    for i in range(4):
        node = TreeNode(f"3_{i+1}", level=3)
        node.left_child = level2[i * 2]
        node.right_child = level2[i * 2 + 1]
        level2[i * 2].parent = node
        level2[i * 2 + 1].parent = node
        level3.append(node)

    # Level 4: Create 2 nodes
    level4 = []
    for i in range(2):
        node = TreeNode(f"4_{i+1}", level=4)
        node.left_child = level3[i * 2]
        node.right_child = level3[i * 2 + 1]
        level3[i * 2].parent = node
        level3[i * 2 + 1].parent = node
        level4.append(node)

    # Level 5: Create root
    root = TreeNode("5_1", level=5)
    root.left_child = level4[0]
    root.right_child = level4[1]
    level4[0].parent = root
    level4[1].parent = root

    return BinaryTree(root, leaves)
