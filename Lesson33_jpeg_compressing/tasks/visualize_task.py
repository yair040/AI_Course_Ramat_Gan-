"""
Visualization task for creating histograms.
Author: Yair Levi
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from ..utils.logger import get_logger
from ..utils.config import (
    PLOTS_DIR,
    HISTOGRAM_DPI,
    HISTOGRAM_FIGSIZE_SINGLE,
)

logger = get_logger(__name__)


def create_file_size_histogram(original_size, compressed_results, output_dir=None):
    """
    Create file size histogram comparing original vs compressed at different Q levels.
    
    Args:
        original_size: Original image size in bytes
        compressed_results: List of (quality, path, size) tuples
        output_dir: Output directory (defaults to PLOTS_DIR)
    """
    if output_dir is None:
        output_dir = PLOTS_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Creating file size histogram")
    
    # Sort by quality
    sorted_results = sorted(compressed_results, key=lambda x: x[0])
    
    # Extract quality levels and file sizes
    qualities = [q for q, _, _ in sorted_results]
    file_sizes_kb = [size / 1024 for _, _, size in sorted_results]
    
    # Original size in KB
    original_size_kb = original_size / 1024
    
    # Create figure
    fig, ax = plt.subplots(figsize=HISTOGRAM_FIGSIZE_SINGLE)
    
    # Create bar positions
    x_positions = list(range(len(qualities) + 1))
    
    # Prepare data: [Original, Q10, Q20, ..., Q95]
    all_sizes = [original_size_kb] + file_sizes_kb
    labels = ['Original'] + [f'Q{q}' for q in qualities]
    colors = ['blue'] + ['red'] * len(qualities)
    
    # Create bar chart
    bars = ax.bar(x_positions, all_sizes, color=colors, alpha=0.7, edgecolor='black')
    
    # Customize plot
    ax.set_xlabel('Quality Level', fontsize=12)
    ax.set_ylabel('File Size (KB)', fontsize=12)
    ax.set_title('File Size: Original vs Compressed at Different Quality Levels', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on top of bars
    for i, (bar, size) in enumerate(zip(bars, all_sizes)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{size:.1f}',
                ha='center', va='bottom', fontsize=8)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='blue', alpha=0.7, label='Original (Uncompressed)'),
        Patch(facecolor='red', alpha=0.7, label='Compressed (JPEG)')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    # Save plot
    plot_path = output_dir / 'file_size_histogram.png'
    plt.tight_layout()
    plt.savefig(plot_path, dpi=HISTOGRAM_DPI)
    plt.close()
    logger.info(f"Saved file size histogram: {plot_path.name}")


def create_error_histogram(metrics_df, output_dir=None):
    """
    Create error histogram showing MSE vs Quality level.
    
    Args:
        metrics_df: DataFrame with error metrics
        output_dir: Output directory (defaults to PLOTS_DIR)
    """
    if output_dir is None:
        output_dir = PLOTS_DIR
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info("Creating error histogram")
    
    # Create figure
    fig, ax = plt.subplots(figsize=HISTOGRAM_FIGSIZE_SINGLE)
    
    # Create bar chart for MSE
    qualities = metrics_df['Quality'].values
    mse_values = metrics_df['MSE'].values
    
    bars = ax.bar(qualities, mse_values, width=8, color='orange', 
                   alpha=0.7, edgecolor='black', label='MSE')
    
    # Customize plot
    ax.set_xlabel('Quality Level (Q)', fontsize=12)
    ax.set_ylabel('Mean Squared Error (MSE)', fontsize=12)
    ax.set_title('Reconstruction Error vs JPEG Quality Level', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(loc='upper right')
    
    # Set x-axis ticks to show all quality levels
    ax.set_xticks(qualities)
    ax.set_xticklabels([f'{int(q)}' for q in qualities])
    
    # Add value labels on top of bars
    for bar, mse in zip(bars, mse_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{mse:.2f}',
                ha='center', va='bottom', fontsize=8, rotation=0)
    
    # Save plot
    plot_path = output_dir / 'error_histogram.png'
    plt.tight_layout()
    plt.savefig(plot_path, dpi=HISTOGRAM_DPI)
    plt.close()
    logger.info(f"Saved error histogram: {plot_path.name}")


# Keep old function names for backwards compatibility but create wrapper
def create_byte_histograms(original, decompressed_results, output_dir=None):
    """
    Deprecated: Use create_file_size_histogram instead.
    This function is kept for compatibility but does nothing.
    """
    logger.warning("create_byte_histograms is deprecated - using new histogram functions")
    pass
