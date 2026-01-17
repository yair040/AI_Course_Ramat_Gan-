"""
Token Manager Module

Handles token assignment and extraction for tree leaves.
Provides functions for random token generation and management.

Author: Yair Levi
"""

import random
from typing import List, Optional, Tuple
from .tree_structure import TreeNode


def assign_random_tokens(
    leaves: List[TreeNode],
    min_val: int = 0,
    max_val: int = 1000,
    seed: Optional[int] = None
) -> None:
    """
    Assign random token values to leaf nodes.

    Args:
        leaves: List of leaf nodes to assign tokens to
        min_val: Minimum token value (inclusive)
        max_val: Maximum token value (inclusive)
        seed: Optional random seed for reproducibility
    """
    if seed is not None:
        random.seed(seed)

    for leaf in leaves:
        leaf.set_tokens(random.randint(min_val, max_val))


def extract_leaf_tokens(leaves: List[TreeNode]) -> List[int]:
    """
    Extract token counts from all leaves.

    Args:
        leaves: List of leaf nodes

    Returns:
        List of token counts from leaves
    """
    return [leaf.token_count for leaf in leaves]


def assign_token_list(leaves: List[TreeNode], tokens: List[int]) -> None:
    """
    Assign a list of token values to leaves in order.

    Args:
        leaves: List of leaf nodes
        tokens: List of token values to assign

    Raises:
        ValueError: If list lengths don't match
    """
    if len(leaves) != len(tokens):
        raise ValueError(
            f"Leaf count ({len(leaves)}) must match token count ({len(tokens)})"
        )

    for leaf, token_count in zip(leaves, tokens):
        leaf.set_tokens(token_count)


def pair_leaves_by_parent(leaves: List[TreeNode]) -> List[Tuple[TreeNode, TreeNode]]:
    """
    Group leaves into pairs based on shared parent.

    Args:
        leaves: List of leaf nodes (must be sorted by name)

    Returns:
        List of (left_child, right_child) tuples
    """
    pairs = []
    for i in range(0, len(leaves), 2):
        if i + 1 < len(leaves):
            pairs.append((leaves[i], leaves[i + 1]))
    return pairs


def assign_token_pairs(
    leaf_pairs: List[Tuple[TreeNode, TreeNode]],
    token_pairs: List[Tuple[int, int]]
) -> None:
    """
    Assign token pairs to leaf pairs.

    Args:
        leaf_pairs: List of (left_leaf, right_leaf) tuples
        token_pairs: List of (left_tokens, right_tokens) tuples

    Raises:
        ValueError: If list lengths don't match
    """
    if len(leaf_pairs) != len(token_pairs):
        raise ValueError(
            f"Leaf pair count ({len(leaf_pairs)}) must match "
            f"token pair count ({len(token_pairs)})"
        )

    for (left_leaf, right_leaf), (left_tokens, right_tokens) in zip(
        leaf_pairs, token_pairs
    ):
        left_leaf.set_tokens(left_tokens)
        right_leaf.set_tokens(right_tokens)
