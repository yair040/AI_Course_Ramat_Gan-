"""Visualization of comparison results.

This module generates publication-quality graphs comparing
Context Window and RAG methods.
"""

from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns
import config
from results_analyzer import calculate_stats
from logger_setup import get_logger

logger = get_logger()

# Set style
sns.set_style("whitegrid")


def plot_response_time(cw_stats: Dict, rag_stats: Dict) -> None:
    """
    Generate response time bar chart with error bars.

    Args:
        cw_stats: Context Window statistics
        rag_stats: RAG statistics
    """
    methods = ["Context Window", "RAG"]
    means = [cw_stats["time_mean"], rag_stats["time_mean"]]
    stds = [cw_stats["time_std"], rag_stats["time_std"]]

    fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)

    bars = ax.bar(methods, means, yerr=stds, capsize=10,
                  color=["#3498db", "#2ecc71"], alpha=0.8, edgecolor="black")

    ax.set_ylabel("Response Time (seconds)", fontsize=12, fontweight="bold")
    ax.set_title("Response Time Comparison: Context Window vs RAG",
                 fontsize=14, fontweight="bold")

    # Add value labels on bars
    for bar, mean in zip(bars, means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'{mean:.2f}s',
                ha='center', va='bottom', fontsize=11, fontweight="bold")

    plt.tight_layout()
    plt.savefig("response_time_comparison.png", dpi=config.DPI, bbox_inches='tight')
    plt.close()
    logger.info("Saved: response_time_comparison.png")


def plot_token_usage(cw_stats: Dict, rag_stats: Dict) -> None:
    """
    Generate token usage grouped bar chart.

    Args:
        cw_stats: Context Window statistics
        rag_stats: RAG statistics
    """
    import numpy as np

    methods = ["Context Window", "RAG"]
    input_tokens = [cw_stats["input_tokens_mean"], rag_stats["input_tokens_mean"]]
    output_tokens = [cw_stats["output_tokens_mean"], rag_stats["output_tokens_mean"]]

    x = np.arange(len(methods))
    width = 0.35

    fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)

    bars1 = ax.bar(x - width/2, input_tokens, width, label='Input Tokens',
                   color="#e74c3c", alpha=0.8, edgecolor="black")
    bars2 = ax.bar(x + width/2, output_tokens, width, label='Output Tokens',
                   color="#9b59b6", alpha=0.8, edgecolor="black")

    ax.set_ylabel("Token Count", fontsize=12, fontweight="bold")
    ax.set_title("Token Usage Comparison", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(methods)
    ax.legend(fontsize=11)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig("token_usage_comparison.png", dpi=config.DPI, bbox_inches='tight')
    plt.close()
    logger.info("Saved: token_usage_comparison.png")


def plot_cost_comparison(cw_stats: Dict, rag_stats: Dict) -> None:
    """
    Generate cost comparison bar chart.

    Args:
        cw_stats: Context Window statistics
        rag_stats: RAG statistics
    """
    methods = ["Context Window", "RAG"]
    costs = [cw_stats["cost_total"], rag_stats["cost_total"]]

    fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)

    bars = ax.bar(methods, costs, color=["#e67e22", "#16a085"],
                  alpha=0.8, edgecolor="black")

    ax.set_ylabel("Total Cost (USD)", fontsize=12, fontweight="bold")
    ax.set_title("Cost Comparison: Context Window vs RAG (5 queries)",
                 fontsize=14, fontweight="bold")

    # Add value labels
    for bar, cost in zip(bars, costs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'${cost:.4f}',
                ha='center', va='bottom', fontsize=11, fontweight="bold")

    # Add savings annotation
    savings = ((costs[0] - costs[1]) / costs[0]) * 100
    ax.text(0.5, max(costs) * 0.7,
            f'RAG saves {savings:.1f}%\n(${costs[0] - costs[1]:.4f})',
            ha='center', fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig("cost_comparison.png", dpi=config.DPI, bbox_inches='tight')
    plt.close()
    logger.info("Saved: cost_comparison.png")


def plot_iterations_timeline(cw_results: List[Dict], rag_results: List[Dict]) -> None:
    """
    Generate iteration timeline line plot.

    Args:
        cw_results: Context Window results
        rag_results: RAG results
    """
    cw_iterations = [r["iteration"] for r in cw_results]
    cw_times = [r["time_seconds"] for r in cw_results]

    rag_iterations = [r["iteration"] for r in rag_results]
    rag_times = [r["time_seconds"] for r in rag_results]

    fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)

    ax.plot(cw_iterations, cw_times, marker='o', linewidth=2, markersize=8,
            label="Context Window", color="#3498db")
    ax.plot(rag_iterations, rag_times, marker='s', linewidth=2, markersize=8,
            label="RAG", color="#2ecc71")

    ax.set_xlabel("Iteration", fontsize=12, fontweight="bold")
    ax.set_ylabel("Response Time (seconds)", fontsize=12, fontweight="bold")
    ax.set_title("Response Time Across Iterations", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("iterations_timeline.png", dpi=config.DPI, bbox_inches='tight')
    plt.close()
    logger.info("Saved: iterations_timeline.png")


def generate_all_graphs(cw_results: List[Dict], rag_results: List[Dict]) -> None:
    """
    Generate all visualization graphs.

    Args:
        cw_results: Context Window results
        rag_results: RAG results
    """
    logger.info("Generating comparison graphs...")

    # Calculate statistics
    cw_stats = calculate_stats(cw_results)
    rag_stats = calculate_stats(rag_results)

    # Generate all plots
    plot_response_time(cw_stats, rag_stats)
    plot_token_usage(cw_stats, rag_stats)
    plot_cost_comparison(cw_stats, rag_stats)
    plot_iterations_timeline(cw_results, rag_results)

    logger.info("All graphs generated successfully")
