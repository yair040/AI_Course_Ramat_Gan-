"""
Visualization module for Iris classification results.
Author: Yair Levi
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from iris_classifier.logger_setup import get_logger
from iris_classifier.config import RESULTS_DIR, FIGURE_DPI, FIGURE_SIZE

logger = get_logger(__name__)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = FIGURE_DPI


def plot_accuracy_distribution(aggregated_stats):
    """Plot accuracy distribution across iterations."""
    logger.info("Creating accuracy distribution plot")
    
    fig, ax = plt.subplots(figsize=FIGURE_SIZE)
    
    stages = ['Stage 1', 'Stage 2', 'Overall']
    means = [
        aggregated_stats['stage1']['accuracy']['mean'],
        aggregated_stats['stage2']['accuracy']['mean'],
        aggregated_stats['overall']['accuracy']['mean']
    ]
    stds = [
        aggregated_stats['stage1']['accuracy']['std'],
        aggregated_stats['stage2']['accuracy']['std'],
        aggregated_stats['overall']['accuracy']['std']
    ]
    
    x_pos = np.arange(len(stages))
    ax.bar(x_pos, means, yerr=stds, align='center', alpha=0.7, 
           ecolor='black', capsize=10, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    
    ax.set_ylabel('Accuracy', fontsize=12)
    ax.set_xlabel('Classification Stage', fontsize=12)
    ax.set_title('Accuracy Distribution Across Stages', fontsize=14, fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(stages)
    ax.set_ylim([0, 1.05])
    ax.axhline(y=0.8, color='r', linestyle='--', alpha=0.3, label='80% baseline')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = RESULTS_DIR / "accuracy_distribution.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Accuracy distribution plot saved to: {output_path}")


def plot_confusion_matrix(all_iterations):
    """Plot aggregated confusion matrix."""
    logger.info("Creating confusion matrix plot")
    
    # Aggregate confusion matrices
    cm_sum = None
    for iteration in all_iterations:
        cm = iteration['overall']['confusion_matrix']
        if cm_sum is None:
            cm_sum = cm.astype(float)
        else:
            cm_sum += cm
    
    # Average
    cm_avg = cm_sum / len(all_iterations)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm_avg, annot=True, fmt='.1f', cmap='Blues', 
                xticklabels=['Setosa', 'Versicolor', 'Virginica'],
                yticklabels=['Setosa', 'Versicolor', 'Virginica'],
                ax=ax, cbar_kws={'label': 'Count'})
    
    ax.set_ylabel('True Label', fontsize=12)
    ax.set_xlabel('Predicted Label', fontsize=12)
    ax.set_title('Average Confusion Matrix (5 iterations)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    output_path = RESULTS_DIR / "confusion_matrix.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Confusion matrix plot saved to: {output_path}")


def plot_metrics_comparison(aggregated_stats):
    """Plot comparison of all metrics across stages."""
    logger.info("Creating metrics comparison plot")
    
    metrics = ['accuracy', 'precision', 'recall', 'f1_score']
    stages = ['stage1', 'stage2', 'overall']
    stage_labels = ['Stage 1', 'Stage 2', 'Overall']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = np.arange(len(metrics))
    width = 0.25
    
    for i, stage in enumerate(stages):
        means = [aggregated_stats[stage][m]['mean'] for m in metrics]
        stds = [aggregated_stats[stage][m]['std'] for m in metrics]
        ax.bar(x + i*width, means, width, yerr=stds, label=stage_labels[i],
               alpha=0.8, capsize=5)
    
    ax.set_ylabel('Score', fontsize=12)
    ax.set_xlabel('Metric', fontsize=12)
    ax.set_title('Performance Metrics Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x + width)
    ax.set_xticklabels(['Accuracy', 'Precision', 'Recall', 'F1-Score'])
    ax.set_ylim([0, 1.05])
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    output_path = RESULTS_DIR / "metrics_comparison.png"
    plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Metrics comparison plot saved to: {output_path}")


def generate_all_plots(all_iterations, aggregated_stats):
    """Generate all visualization plots."""
    logger.info("Generating all visualization plots")
    
    try:
        plot_accuracy_distribution(aggregated_stats)
        plot_confusion_matrix(all_iterations)
        plot_metrics_comparison(aggregated_stats)
        logger.info("All plots generated successfully")
    except Exception as e:
        logger.error(f"Error generating plots: {e}")
        raise