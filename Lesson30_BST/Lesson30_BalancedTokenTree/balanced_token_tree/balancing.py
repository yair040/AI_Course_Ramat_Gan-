"""
Balancing Algorithm Module

Implements the tree balancing algorithm that pairs extreme token values
to minimize variance across parent nodes.

Author: Yair Levi
"""

import logging
from typing import List, Tuple, Dict, Any
from .tree_structure import BinaryTree
from .token_manager import (
    extract_leaf_tokens,
    pair_leaves_by_parent,
    assign_token_pairs
)

logger = logging.getLogger(__name__)


def sort_tokens(tokens: List[int]) -> List[int]:
    """
    Sort token values in ascending order.

    Args:
        tokens: List of token values

    Returns:
        Sorted list of tokens
    """
    return sorted(tokens)


def create_balanced_pairs(sorted_tokens: List[int]) -> List[Tuple[int, int]]:
    """
    Create balanced pairs by matching smallest with largest values.

    This algorithm pairs extremes to minimize variance in parent node sums.

    Args:
        sorted_tokens: Sorted list of token values

    Returns:
        List of (small, large) token pairs

    Example:
        [100, 200, 300, 400] -> [(100, 400), (200, 300)]
    """
    tokens = sorted_tokens.copy()
    pairs = []

    while len(tokens) >= 2:
        smallest = tokens.pop(0)  # Remove first (smallest)
        largest = tokens.pop()     # Remove last (largest)
        pairs.append((smallest, largest))

    return pairs


def calculate_statistics(tree: BinaryTree) -> Dict[str, Any]:
    """
    Calculate statistical measures for tree token distribution.

    Args:
        tree: Binary tree to analyze

    Returns:
        Dictionary with statistics (total, variance by level, etc.)
    """
    stats = {
        'total_tokens': tree.root.token_count,
        'levels': {}
    }

    # Calculate statistics for each level
    for level in range(1, 6):
        nodes = tree.get_nodes_by_level(level)
        token_counts = [node.token_count for node in nodes]

        if token_counts:
            mean = sum(token_counts) / len(token_counts)
            variance = sum((x - mean) ** 2 for x in token_counts) / len(token_counts)
            std_dev = variance ** 0.5

            stats['levels'][level] = {
                'node_count': len(nodes),
                'mean': mean,
                'variance': variance,
                'std_dev': std_dev,
                'min': min(token_counts),
                'max': max(token_counts)
            }

    return stats


def apply_balancing(tree: BinaryTree, iteration: int) -> Dict[str, Any]:
    """
    Apply the balancing algorithm to redistribute tokens.

    Args:
        tree: Binary tree to balance
        iteration: Iteration number (for logging)

    Returns:
        Statistics dictionary after balancing
    """
    logger.info(f"Applying balancing algorithm (Iteration {iteration})")

    # Step 1: Extract current leaf tokens
    original_tokens = extract_leaf_tokens(tree.leaves)
    original_total = sum(original_tokens)
    logger.info(f"Original total tokens: {original_total}")

    # Step 2: Sort tokens
    sorted_tokens = sort_tokens(original_tokens)
    logger.debug(f"Sorted tokens: {sorted_tokens[:5]}...{sorted_tokens[-5:]}")

    # Step 3: Create balanced pairs
    token_pairs = create_balanced_pairs(sorted_tokens)
    logger.info(f"Created {len(token_pairs)} balanced pairs")

    # Step 4: Reset tree tokens
    tree.reset_tokens()

    # Step 5: Pair leaves by parent
    leaf_pairs = pair_leaves_by_parent(tree.get_all_leaves_sorted())

    # Step 6: Assign balanced token pairs to leaf pairs
    assign_token_pairs(leaf_pairs, token_pairs)

    # Step 7: Recalculate sums from leaves to root
    tree.calculate_all_sums()

    # Verify token conservation
    final_total = tree.root.token_count
    if final_total != original_total:
        logger.error(
            f"Token count mismatch! Original: {original_total}, "
            f"Final: {final_total}"
        )
        raise ValueError("Token conservation violated during balancing")

    logger.info(f"Balancing complete. Total tokens preserved: {final_total}")

    # Calculate and return statistics
    stats = calculate_statistics(tree)
    return stats
