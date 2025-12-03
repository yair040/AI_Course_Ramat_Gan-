"""
Visualization Module

Creates histogram plots for feature distributions and confusion matrices
for model evaluation.

Author: Yair Levi
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for WSL compatibility
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
import logging


logger = logging.getLogger('iris_classifier')


def plot_histograms(histogram_data, feature_names, class_names, save_path='histograms.png'):
    """
    Plot histograms for all features across all classes.

    Creates a 2x2 grid showing one feature per subplot, with all classes
    overlaid in different colors.

    Args:
        histogram_data: Dictionary {class: {feature_idx: (counts, edges)}}
        feature_names: List of feature names
        class_names: List of class names
        save_path: Path to save the figure (default: 'histograms.png')
    """
    logger.info("Creating histogram visualizations")

    n_features = len(feature_names)
    colors = ['blue', 'green', 'red']

    # Create 2x2 subplot grid
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for feature_idx in range(n_features):
        ax = axes[feature_idx]

        # Plot histogram for each class
        for class_idx, class_name in enumerate(class_names):
            counts, bin_edges = histogram_data[class_name][feature_idx]

            # Calculate bin centers for bar plot
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
            bin_width = bin_edges[1] - bin_edges[0]

            # Plot as bars with transparency
            ax.bar(bin_centers, counts, width=bin_width * 0.8,
                   alpha=0.5, color=colors[class_idx],
                   label=class_name, edgecolor='black')

        # Formatting
        ax.set_xlabel(feature_names[feature_idx], fontsize=11)
        ax.set_ylabel('Frequency (with Laplace smoothing)', fontsize=11)
        ax.set_title(f'Distribution of {feature_names[feature_idx]}', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    logger.info(f"Histograms saved to: {save_path}")
    plt.close()


def plot_confusion_matrix(y_true, y_pred, class_names, title='Confusion Matrix',
                          ax=None, save_path=None):
    """
    Plot confusion matrix as a heatmap.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        class_names: List of class names
        title: Plot title
        ax: Matplotlib axis (if None, creates new figure)
        save_path: Path to save figure (optional)

    Returns:
        Matplotlib axis
    """
    # Calculate confusion matrix
    cm = confusion_matrix(y_true, y_pred, labels=class_names)

    # Create new figure if no axis provided
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))

    # Plot heatmap
    im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
    ax.figure.colorbar(im, ax=ax)

    # Configure ticks
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=class_names,
           yticklabels=class_names,
           title=title,
           ylabel='True Label',
           xlabel='Predicted Label')

    # Rotate x-axis labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black",
                   fontsize=14, fontweight='bold')

    # Save if path provided and no existing axis
    if save_path and ax is None:
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        logger.info(f"Confusion matrix saved to: {save_path}")
        plt.close()

    return ax


def display_results(y_test, y_pred_manual, y_pred_library, class_names,
                   save_path='confusion_matrices.png'):
    """
    Display side-by-side confusion matrices and accuracy comparison.

    Args:
        y_test: True test labels
        y_pred_manual: Predictions from manual implementation
        y_pred_library: Predictions from library implementation
        class_names: List of class names
        save_path: Path to save the figure
    """
    logger.info("Generating comparison results")

    # Calculate accuracies
    acc_manual = accuracy_score(y_test, y_pred_manual)
    acc_library = accuracy_score(y_test, y_pred_library)

    logger.info(f"Manual Implementation Accuracy: {acc_manual:.4f}")
    logger.info(f"Library Implementation Accuracy: {acc_library:.4f}")

    # Print to console
    print("\n" + "="*60)
    print("CLASSIFICATION RESULTS")
    print("="*60)
    print(f"Manual Implementation Accuracy:  {acc_manual:.2%}")
    print(f"Library Implementation Accuracy: {acc_library:.2%}")
    print(f"Difference: {abs(acc_manual - acc_library):.2%}")
    print("="*60 + "\n")

    # Create side-by-side confusion matrices
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot manual implementation
    plot_confusion_matrix(y_test, y_pred_manual, class_names,
                         title=f'Manual Implementation\nAccuracy: {acc_manual:.2%}',
                         ax=ax1)

    # Plot library implementation
    plot_confusion_matrix(y_test, y_pred_library, class_names,
                         title=f'Library Implementation\nAccuracy: {acc_library:.2%}',
                         ax=ax2)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    logger.info(f"Comparison results saved to: {save_path}")
    plt.close()

    logger.info("Results display completed")
