"""
Visualization functions for semantic clustering system.
Author: Yair Levi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from typing import List, Tuple


def create_cluster_visualization(
    vectors: np.ndarray,
    labels: np.ndarray,
    centroids: np.ndarray,
    title: str,
    save_path: str = None
) -> None:
    """
    Create 2D visualization of clusters using PCA.

    Args:
        vectors: Input vectors (n_samples, n_features)
        labels: Cluster labels (n_samples,)
        centroids: Cluster centroids (n_clusters, n_features)
        title: Plot title
        save_path: Optional path to save the figure
    """
    # Reduce to 2D using PCA
    pca = PCA(n_components=2)
    vectors_2d = pca.fit_transform(vectors)
    centroids_2d = pca.transform(centroids)

    # Create figure
    plt.figure(figsize=(12, 8))

    # Define colors for clusters
    colors = ['#8B0000', '#006400', '#00008B']
    cluster_names = ['Cluster 0', 'Cluster 1', 'Cluster 2']

    # Plot each cluster
    for i in range(3):
        cluster_points = vectors_2d[labels == i]
        plt.scatter(
            cluster_points[:, 0],
            cluster_points[:, 1],
            c=colors[i],
            label=cluster_names[i],
            alpha=0.6,
            s=100,
            edgecolors='black',
            linewidth=0.5
        )

    # Plot centroids
    plt.scatter(
        centroids_2d[:, 0],
        centroids_2d[:, 1],
        c='red',
        marker='X',
        s=500,
        edgecolors='black',
        linewidth=2,
        label='Centroids',
        zorder=10
    )

    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)', fontsize=12)
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to: {save_path}")

    plt.show()


def create_cluster_table(
    sentences: List[str],
    labels: np.ndarray,
    subjects: List[str] = None
) -> pd.DataFrame:
    """
    Create a table showing cluster assignments.

    Args:
        sentences: List of sentences
        labels: Cluster labels
        subjects: Optional list of actual subjects

    Returns:
        DataFrame with cluster information
    """
    data = {
        'Index': range(len(sentences)),
        'Sentence': sentences,
        'Cluster': labels
    }

    if subjects:
        data['Actual_Subject'] = subjects

    df = pd.DataFrame(data)

    return df


def print_cluster_summary(
    df: pd.DataFrame,
    title: str = "Cluster Summary"
) -> None:
    """
    Print summary statistics for clusters.

    Args:
        df: DataFrame with cluster information
        title: Title for the summary
    """
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")

    # Count by cluster
    cluster_counts = df['Cluster'].value_counts().sort_index()
    print("\nSentences per cluster:")
    for cluster, count in cluster_counts.items():
        print(f"  Cluster {cluster}: {count} sentences")

    # If we have actual subjects, show distribution
    if 'Actual_Subject' in df.columns:
        print("\nSubject distribution per cluster:")
        for cluster in sorted(df['Cluster'].unique()):
            cluster_df = df[df['Cluster'] == cluster]
            subject_counts = cluster_df['Actual_Subject'].value_counts()
            print(f"\n  Cluster {cluster}:")
            for subject, count in subject_counts.items():
                percentage = (count / len(cluster_df)) * 100
                print(f"    {subject}: {count} ({percentage:.1f}%)")

    print(f"{'='*80}\n")


def display_cluster_samples(
    df: pd.DataFrame,
    n_samples: int = 3,
    title: str = "Sample Sentences per Cluster"
) -> None:
    """
    Display sample sentences from each cluster.

    Args:
        df: DataFrame with cluster information
        n_samples: Number of samples to show per cluster
        title: Title for the display
    """
    print(f"\n{'='*80}")
    print(f"{title}")
    print(f"{'='*80}")

    for cluster in sorted(df['Cluster'].unique()):
        cluster_df = df[df['Cluster'] == cluster]
        samples = cluster_df.head(n_samples)

        print(f"\nCluster {cluster} (showing {min(n_samples, len(cluster_df))} of {len(cluster_df)}):")
        print("-" * 80)

        for idx, row in samples.iterrows():
            subject_info = f" [{row['Actual_Subject']}]" if 'Actual_Subject' in df.columns else ""
            print(f"  {row['Index']:3d}. {row['Sentence']}{subject_info}")

    print(f"{'='*80}\n")


def save_table_to_csv(df: pd.DataFrame, save_path: str) -> None:
    """
    Save DataFrame to CSV file.

    Args:
        df: DataFrame to save
        save_path: Path to save the CSV file
    """
    df.to_csv(save_path, index=False)
    print(f"Saved table to: {save_path}")


def create_confusion_matrix(
    df: pd.DataFrame,
    save_path: str = None
) -> None:
    """
    Create confusion matrix if actual subjects are available.

    Args:
        df: DataFrame with 'Actual_Subject' and 'Cluster' columns
        save_path: Optional path to save the figure
    """
    if 'Actual_Subject' not in df.columns:
        print("Cannot create confusion matrix: Actual subjects not available")
        return

    # Create contingency table
    contingency = pd.crosstab(
        df['Actual_Subject'],
        df['Cluster'],
        margins=True,
        margins_name='Total'
    )

    # Create heatmap
    plt.figure(figsize=(10, 7))
    sns.heatmap(
        contingency.iloc[:-1, :-1],  # Exclude margins
        annot=True,
        fmt='d',
        cmap='YlOrRd',
        cbar_kws={'label': 'Count'},
        linewidths=1,
        linecolor='black'
    )

    plt.title('Subject vs Cluster Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Cluster', fontsize=12)
    plt.ylabel('Actual Subject', fontsize=12)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved confusion matrix to: {save_path}")

    plt.show()

    # Print the contingency table
    print("\nContingency Table:")
    print(contingency)
    print()
