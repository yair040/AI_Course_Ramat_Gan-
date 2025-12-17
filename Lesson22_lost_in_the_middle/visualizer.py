"""
Visualizer Module

Creates visualizations of experiment results.

Author: Yair Levi
"""

from typing import Dict

import matplotlib.pyplot as plt

from config import (
    TEST_ITERATIONS,
    DOCUMENTS_PER_POSITION,
    CHART_TITLE,
    CHART_XLABEL,
    CHART_YLABEL,
    CHART_COLORS,
    CHART_DPI,
    CHART_FIGSIZE,
    get_results_graph_path
)
from utils import get_logger


logger = get_logger(__name__)


# ============================================================================
# CHART CREATION
# ============================================================================

def create_bar_chart(counters: Dict[str, int], iterations: int = TEST_ITERATIONS):
    """
    Create bar chart visualization of results.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations

    Returns:
        Matplotlib figure object
    """
    logger.info("Creating bar chart visualization...")

    # Calculate success rates
    tests_per_position = DOCUMENTS_PER_POSITION * iterations
    positions = ['Start', 'Middle', 'End']
    position_keys = ['start', 'middle', 'end']

    success_rates = [
        (counters[key] / tests_per_position) * 100
        for key in position_keys
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE)

    # Create bars
    bars = ax.bar(
        positions,
        success_rates,
        color=CHART_COLORS,
        alpha=0.8,
        edgecolor='black',
        linewidth=1.5
    )

    # Customize chart
    ax.set_ylabel(CHART_YLABEL, fontsize=12, fontweight='bold')
    ax.set_xlabel(CHART_XLABEL, fontsize=12, fontweight='bold')
    ax.set_title(CHART_TITLE, fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)

    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Add value labels on bars
    for bar, rate in zip(bars, success_rates):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{rate:.1f}%',
            ha='center',
            va='bottom',
            fontsize=12,
            fontweight='bold'
        )

    # Add test details
    details_text = f"Iterations: {iterations} | Tests per position: {tests_per_position}"
    ax.text(
        0.5,
        -0.15,
        details_text,
        ha='center',
        transform=ax.transAxes,
        fontsize=10,
        style='italic'
    )

    # Tight layout
    plt.tight_layout()

    logger.info("Bar chart created successfully")

    return fig


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def save_chart(fig, filename: str = None) -> None:
    """
    Save chart to results directory.

    Args:
        fig: Matplotlib figure object
        filename: Optional custom filename
    """
    if filename is None:
        output_path = get_results_graph_path()
    else:
        output_path = get_results_graph_path().parent / filename

    try:
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Save figure
        fig.savefig(
            output_path,
            dpi=CHART_DPI,
            bbox_inches='tight',
            facecolor='white'
        )

        logger.info(f"Chart saved to: {output_path}")

    except Exception as e:
        logger.error(f"Error saving chart: {e}")
        raise


def display_chart(fig) -> None:
    """
    Display chart (if in interactive environment).

    Args:
        fig: Matplotlib figure object
    """
    try:
        plt.show()
        logger.info("Chart displayed")
    except Exception as e:
        logger.warning(f"Could not display chart: {e}")


# ============================================================================
# MAIN VISUALIZATION WORKFLOW
# ============================================================================

def visualize_results(
    counters: Dict[str, int],
    iterations: int = TEST_ITERATIONS,
    save: bool = True,
    display: bool = False
) -> None:
    """
    Complete visualization workflow.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations
        save: Whether to save the chart
        display: Whether to display the chart
    """
    logger.info("="*60)
    logger.info("VISUALIZATION")
    logger.info("="*60)

    # Create chart
    fig = create_bar_chart(counters, iterations)

    # Save if requested
    if save:
        save_chart(fig)

    # Display if requested
    if display:
        display_chart(fig)
    else:
        # Close figure to free memory
        plt.close(fig)

    logger.info("="*60)
    logger.info("Visualization complete")
    logger.info("="*60)


# ============================================================================
# ADDITIONAL VISUALIZATIONS
# ============================================================================

def create_comparison_table(counters: Dict[str, int], iterations: int) -> str:
    """
    Create ASCII table comparing results.

    Args:
        counters: Dictionary of success counts by position
        iterations: Number of test iterations

    Returns:
        Formatted table string
    """
    tests_per_position = DOCUMENTS_PER_POSITION * iterations

    lines = [
        "+------------+----------+-------------+",
        "| Position   | Correct  | Success (%) |",
        "+------------+----------+-------------+"
    ]

    for position in ['start', 'middle', 'end']:
        count = counters[position]
        rate = (count / tests_per_position) * 100
        lines.append(f"| {position.capitalize():10} | {count:2}/{tests_per_position:2} | {rate:10.1f}% |")

    lines.append("+------------+----------+-------------+")

    return '\n'.join(lines)
