"""
Visualization Module

Generates graphs and displays results from the context window testing.
Creates dual-axis plots showing query time and accuracy vs token count.

Author: Yair Levi
"""

from typing import List, Dict
import matplotlib.pyplot as plt
import numpy as np
import config
from logger_setup import get_logger

logger = get_logger()


def prepare_data(results_list: List[Dict]) -> Dict:
    """
    Extract data arrays from results list for plotting.

    Args:
        results_list: List of result dictionaries

    Returns:
        Dictionary with arrays for plotting:
        {
            "tokens": token counts,
            "times": query times,
            "accuracies": accuracy values,
            "words": word counts,
            "similarities": similarity scores
        }
    """
    token_counts = [r["token_count"] for r in results_list]
    query_times = [r["query_time"] for r in results_list]
    accuracies = [r["accuracy"] for r in results_list]
    word_counts = [r["word_count"] for r in results_list]
    similarities = [r["similarity_score"] for r in results_list]

    return {
        "tokens": token_counts,
        "times": query_times,
        "accuracies": accuracies,
        "words": word_counts,
        "similarities": similarities
    }


def create_dual_axis_plot(data: Dict) -> plt.Figure:
    """
    Create a dual-axis plot showing query time and accuracy vs token count.

    Args:
        data: Dictionary with plotting data

    Returns:
        Matplotlib figure object
    """
    # Create figure and primary axis
    fig, ax1 = plt.subplots(figsize=config.GRAPH_FIGSIZE)

    # Plot query time on left y-axis
    color_time = 'tab:blue'
    ax1.set_xlabel('Token Count', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Query Time (seconds)', color=color_time, fontsize=12, fontweight='bold')
    ax1.plot(data["tokens"], data["times"], color=color_time, marker='o',
             linewidth=2, markersize=8, label='Query Time', linestyle='-')
    ax1.tick_params(axis='y', labelcolor=color_time)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Format x-axis to show token counts clearly
    ax1.ticklabel_format(style='plain', axis='x')

    # Create secondary y-axis for accuracy
    ax2 = ax1.twinx()
    color_accuracy = 'tab:red'
    ax2.set_ylabel('Accuracy (0 or 1)', color=color_accuracy, fontsize=12, fontweight='bold')
    ax2.scatter(data["tokens"], data["accuracies"], color=color_accuracy,
                s=150, marker='s', label='Accuracy', zorder=5, edgecolors='black', linewidth=1.5)
    ax2.set_ylim(-0.1, 1.1)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Incorrect (0)', 'Correct (1)'])
    ax2.tick_params(axis='y', labelcolor=color_accuracy)

    # Add title
    plt.title(config.GRAPH_TITLE, fontsize=14, fontweight='bold', pad=20)

    # Combine legends from both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    return fig


def save_graph(fig: plt.Figure, filename: str):
    """
    Save the graph to a file.

    Args:
        fig: Matplotlib figure object
        filename: Output filename
    """
    try:
        fig.savefig(filename, dpi=config.GRAPH_DPI, bbox_inches='tight')
        logger.info(f"Graph saved to {filename}")

    except Exception as e:
        logger.error(f"Error saving graph: {e}")
        raise


def print_results_table(results_list: List[Dict]):
    """
    Print a formatted table of results to the console.

    Args:
        results_list: List of result dictionaries
    """
    # Print header
    print("\n" + "="*90)
    print(" "*30 + "RESULTS SUMMARY")
    print("="*90)

    # Print column headers
    print(f"{'Document':<18} {'Words':>10} {'Tokens':>12} {'Time (s)':>10} "
          f"{'Accuracy':>10} {'Similarity':>12}")
    print("-"*90)

    # Print each result
    for result in results_list:
        accuracy_symbol = "✓" if result['accuracy'] == 1 else "✗"
        print(f"{result['document_name']:<18} "
              f"{result['word_count']:>10,} "
              f"{result['token_count']:>12,} "
              f"{result['query_time']:>10.2f} "
              f"{accuracy_symbol:>5} ({result['accuracy']})  "
              f"{result['similarity_score']:>11.4f}")

    print("="*90)

    # Calculate and print summary statistics
    total_time = sum(r["query_time"] for r in results_list)
    avg_accuracy = sum(r["accuracy"] for r in results_list) / len(results_list)
    correct_count = sum(1 for r in results_list if r["accuracy"] == 1)
    incorrect_count = len(results_list) - correct_count

    print(f"\nTotal Query Time: {total_time:.2f} seconds")
    print(f"Average Accuracy: {avg_accuracy:.1%} ({correct_count} correct, {incorrect_count} incorrect)")

    # Show threshold information
    print(f"\nSimilarity Threshold: {config.SIMILARITY_THRESHOLD:.2f}")
    print(f"Hypothesis: Accuracy should decrease as document size increases")

    # Check if hypothesis is supported
    if results_list[-1]["accuracy"] < results_list[0]["accuracy"]:
        print("\n⚠ Hypothesis SUPPORTED: Accuracy decreased for larger documents")
    else:
        print("\n✓ Hypothesis NOT SUPPORTED: Accuracy remained consistent")

    print("="*90 + "\n")


def visualize_results(results_list: List[Dict]):
    """
    Main visualization function.

    Creates graph and displays results table.

    Args:
        results_list: List of result dictionaries from document processing
    """
    logger.info("Generating visualization...")

    try:
        # Prepare data
        data = prepare_data(results_list)

        # Create plot
        fig = create_dual_axis_plot(data)

        # Save graph
        save_graph(fig, config.OUTPUT_GRAPH)

        # Close figure to free memory
        plt.close(fig)

        # Print results table
        print_results_table(results_list)

        logger.info("Visualization complete")

    except Exception as e:
        logger.error(f"Error during visualization: {e}")
        raise
