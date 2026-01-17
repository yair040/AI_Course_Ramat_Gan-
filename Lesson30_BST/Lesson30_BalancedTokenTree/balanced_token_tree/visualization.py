"""
Visualization Module

Creates graphical representations of the binary tree with token counts.
Uses matplotlib for rendering and saves to PNG files.

Author: Yair Levi
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for WSL compatibility

import matplotlib.pyplot as plt
import logging
from pathlib import Path
from typing import Dict, Tuple
from .tree_structure import BinaryTree, TreeNode

logger = logging.getLogger(__name__)


def calculate_node_positions(tree: BinaryTree) -> Dict[str, Tuple[float, float]]:
    """
    Calculate x, y positions for all nodes in the tree.

    Uses a layout where leaves are evenly spaced on x-axis,
    and parents are centered between their children.

    Args:
        tree: Binary tree to layout

    Returns:
        Dictionary mapping node name to (x, y) coordinates
    """
    positions = {}

    # Get leaves sorted by name for consistent ordering
    leaves = tree.get_all_leaves_sorted()
    x_spacing = 1.0

    # Position leaves at y=0, evenly spaced on x-axis
    for i, leaf in enumerate(leaves):
        positions[leaf.name] = (i * x_spacing, 0)

    # Position internal nodes level by level
    for level in range(2, 6):
        nodes = tree.get_nodes_by_level(level)
        for node in nodes:
            if node.left_child and node.right_child:
                left_x, left_y = positions[node.left_child.name]
                right_x, right_y = positions[node.right_child.name]
                # Center parent between children
                x = (left_x + right_x) / 2
                y = level - 1
                positions[node.name] = (x, y)

    return positions


def draw_tree(
    tree: BinaryTree,
    output_path: str,
    title: str,
    stats: Dict = None
) -> None:
    """
    Draw the tree and save to file.

    Args:
        tree: Binary tree to visualize
        output_path: Path to save the image
        title: Title for the visualization
        stats: Optional statistics dictionary
    """
    logger.info(f"Generating tree visualization: {title}")

    # Create figure
    fig, ax = plt.subplots(figsize=(20, 12))

    # Calculate positions
    positions = calculate_node_positions(tree)

    # Draw edges first (so they appear behind nodes)
    for node in tree.all_nodes:
        if not node.is_leaf():
            x1, y1 = positions[node.name]

            # Draw edge to left child
            if node.left_child:
                x2, y2 = positions[node.left_child.name]
                ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.6)

            # Draw edge to right child
            if node.right_child:
                x3, y3 = positions[node.right_child.name]
                ax.plot([x1, x3], [y1, y3], 'k-', linewidth=1.5, alpha=0.6)

    # Draw nodes
    for node in tree.all_nodes:
        x, y = positions[node.name]

        # Color by level
        if node.is_leaf():
            color = 'lightblue'
            size = 1200
        elif node.level == 5:
            color = 'lightcoral'
            size = 1500
        else:
            color = 'lightgreen'
            size = 1300

        # Draw node circle
        ax.scatter(x, y, s=size, c=color, edgecolors='black',
                   linewidths=2, zorder=3, alpha=0.8)

        # Add label with name and token count
        label = f"{node.name}\n{node.token_count}"
        ax.text(x, y, label, ha='center', va='center',
                fontsize=9, fontweight='bold', zorder=4)

    # Add title with statistics if provided
    if stats and 'levels' in stats:
        level2_stats = stats['levels'].get(2, {})
        variance = level2_stats.get('variance', 0)
        title_text = f"{title}\nTotal: {stats['total_tokens']} | Level 2 Variance: {variance:.1f}"
    else:
        title_text = title

    ax.set_title(title_text, fontsize=16, fontweight='bold', pad=20)

    # Configure axes
    ax.axis('equal')
    ax.axis('off')

    # Adjust layout
    plt.tight_layout()

    # Create output directory if needed
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    logger.info(f"Visualization saved to: {output_path}")
