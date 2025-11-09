"""
3D visualization functions for clustering results
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# Color palette for clusters (colorblind-friendly)
COLORS = ['#FF6B6B', '#66BB6A', '#2196F3']
FIGURE_SIZE = (12, 9)
POINT_SIZE = 50
LABEL_FONT_SIZE = 6


def plot_3d_clusters(
    points_3d: np.ndarray,
    labels: np.ndarray,
    title: str,
    sentence_ids: np.ndarray = None,
    save_path: str = None,
    show: bool = True
):
    """
    Create 3D scatter plot with cluster colors

    Args:
        points_3d: (N, 3) array of 3D points
        labels: (N,) array of cluster labels
        title: Plot title
        sentence_ids: Optional (N,) array of sentence IDs to display
        save_path: Optional path to save figure
        show: Whether to display plot interactively
    """
    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(111, projection='3d')

    # Get unique clusters
    unique_labels = np.unique(labels)
    n_clusters = len(unique_labels)

    # Plot each cluster with different color
    for i, cluster_label in enumerate(unique_labels):
        mask = labels == cluster_label
        cluster_points = points_3d[mask]

        # Select color
        color = COLORS[i % len(COLORS)]

        # Plot points
        ax.scatter(
            cluster_points[:, 0],
            cluster_points[:, 1],
            cluster_points[:, 2],
            c=color,
            label=f'Cluster {cluster_label}',
            s=POINT_SIZE,
            alpha=0.6,
            edgecolors='black',
            linewidth=0.5
        )

        # Add point labels if requested
        if sentence_ids is not None:
            cluster_ids = sentence_ids[mask]
            for j, point_id in enumerate(cluster_ids):
                ax.text(
                    cluster_points[j, 0],
                    cluster_points[j, 1],
                    cluster_points[j, 2],
                    str(point_id),
                    fontsize=LABEL_FONT_SIZE,
                    alpha=0.7
                )

    # Configure plot
    configure_3d_axes(ax, title)

    # Add legend
    ax.legend(loc='upper right', fontsize=10)

    # Tight layout
    plt.tight_layout()

    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  💾 Plot saved to {save_path}")

    # Show if requested
    if show:
        plt.show()

    return fig, ax


def configure_3d_axes(ax, title: str):
    """
    Configure 3D plot styling

    Args:
        ax: Matplotlib 3D axes
        title: Plot title
    """
    # Set labels
    ax.set_xlabel('Component 1', fontsize=11, labelpad=10)
    ax.set_ylabel('Component 2', fontsize=11, labelpad=10)
    ax.set_zlabel('Component 3', fontsize=11, labelpad=10)

    # Set title
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    # Configure grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # Set background color
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # Set viewing angle
    ax.view_init(elev=20, azim=45)


def plot_comparison(
    results_dict: dict,
    save_path: str = None,
    show: bool = True
):
    """
    Create side-by-side comparison of multiple dimensionality reduction methods

    Args:
        results_dict: Dictionary with keys as method names and values as tuples
                     (points_3d, labels)
        save_path: Optional path to save figure
        show: Whether to display plot
    """
    n_methods = len(results_dict)
    fig = plt.figure(figsize=(15, 5))

    for idx, (method_name, (points_3d, labels)) in enumerate(results_dict.items(), 1):
        ax = fig.add_subplot(1, n_methods, idx, projection='3d')

        # Get unique clusters
        unique_labels = np.unique(labels)

        # Plot each cluster
        for i, cluster_label in enumerate(unique_labels):
            mask = labels == cluster_label
            cluster_points = points_3d[mask]

            color = COLORS[i % len(COLORS)]

            ax.scatter(
                cluster_points[:, 0],
                cluster_points[:, 1],
                cluster_points[:, 2],
                c=color,
                label=f'Cluster {cluster_label}',
                s=30,
                alpha=0.6,
                edgecolors='black',
                linewidth=0.3
            )

        # Configure
        configure_3d_axes(ax, method_name)
        ax.legend(loc='upper right', fontsize=8)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"  💾 Comparison plot saved to {save_path}")

    if show:
        plt.show()

    return fig
