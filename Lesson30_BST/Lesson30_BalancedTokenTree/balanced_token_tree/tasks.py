"""
Task Orchestration Module - Coordinates the complete workflow.
Author: Yair Levi
"""

import logging
from typing import Optional, Dict, Any
from .tree_structure import BinaryTree, build_tree
from .token_manager import assign_random_tokens
from .balancing import apply_balancing, calculate_statistics
from .visualization import draw_tree

logger = logging.getLogger(__name__)


def task_create_tree() -> BinaryTree:
    """Create the initial tree structure."""
    logger.info("Creating tree structure (5 levels, 16 leaves)")
    tree = build_tree()
    logger.info(f"Tree created: {len(tree.leaves)} leaves, {len(tree.all_nodes)} total nodes")
    return tree


def task_initial_tokens(tree: BinaryTree, seed: Optional[int] = None) -> int:
    """Assign initial random tokens to leaves."""
    logger.info("Assigning random tokens to leaves (0-1000)")
    if seed is not None:
        logger.info(f"Using random seed: {seed}")
    assign_random_tokens(tree.leaves, min_val=0, max_val=1000, seed=seed)
    tree.calculate_all_sums()
    total = tree.root.token_count
    logger.info(f"Initial tokens assigned - Total: {total}")
    return total


def task_balance_iteration(tree: BinaryTree, iteration: int) -> Dict[str, Any]:
    """Perform one balancing iteration."""
    logger.info(f"=== Balancing Iteration {iteration} ===")
    stats = apply_balancing(tree, iteration)

    # Log statistics for level 2 (parent nodes of leaves)
    if 'levels' in stats and 2 in stats['levels']:
        level2 = stats['levels'][2]
        logger.info(f"Level 2 stats: Mean={level2['mean']:.2f}, "
                   f"Variance={level2['variance']:.2f}, "
                   f"Range=[{level2['min']}, {level2['max']}]")
    return stats


def task_visualize(tree: BinaryTree, iteration: int, label: str,
                   stats: Optional[Dict[str, Any]] = None) -> None:
    """Generate and save tree visualization."""
    output_path = f"output/tree_iteration_{iteration}_{label}.png"
    title = f"Tree - Iteration {iteration} ({label.capitalize()})"
    draw_tree(tree, output_path, title, stats)


def run_pipeline(seed: Optional[int] = None) -> None:
    """
    Run the complete balancing pipeline with 2 iterations.

    Each iteration: Random tokens -> Visualize -> Balance -> Visualize
    """
    logger.info("=" * 60)
    logger.info("Starting Balanced Token Tree Pipeline")
    logger.info("=" * 60)

    try:
        # Task 1: Create tree
        tree = task_create_tree()

        # === ITERATION 0 ===
        logger.info("\n" + "=" * 60)
        logger.info("ITERATION 0")
        logger.info("=" * 60)

        # Assign random tokens
        logger.info("Step 1: Assigning random tokens")
        initial_total = task_initial_tokens(tree, seed=seed)
        initial_stats = calculate_statistics(tree)
        task_visualize(tree, 0, "initial", initial_stats)

        # Balance the tree
        logger.info("Step 2: Applying balancing algorithm")
        stats0_balanced = task_balance_iteration(tree, 0)
        task_visualize(tree, 0, "balanced", stats0_balanced)

        # === ITERATION 1 ===
        logger.info("\n" + "=" * 60)
        logger.info("ITERATION 1 (New Random Distribution)")
        logger.info("=" * 60)

        # Assign NEW random tokens (use modified seed if provided)
        logger.info("Step 1: Assigning NEW random tokens")
        new_seed = (seed + 1000) if seed is not None else None
        iteration1_total = task_initial_tokens(tree, seed=new_seed)
        iteration1_stats = calculate_statistics(tree)
        task_visualize(tree, 1, "initial", iteration1_stats)

        # Balance the tree
        logger.info("Step 2: Applying balancing algorithm")
        stats1_balanced = task_balance_iteration(tree, 1)
        task_visualize(tree, 1, "balanced", stats1_balanced)

        # Summary
        logger.info("\n" + "=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info("=" * 60)
        logger.info("Visualizations saved:")
        logger.info("  - output/tree_iteration_0_initial.png")
        logger.info("  - output/tree_iteration_0_balanced.png")
        logger.info("  - output/tree_iteration_1_initial.png")
        logger.info("  - output/tree_iteration_1_balanced.png")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise
