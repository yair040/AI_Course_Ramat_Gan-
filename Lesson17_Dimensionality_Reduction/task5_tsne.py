"""
Task 5: t-SNE dimensionality reduction
"""

import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from utils import (
    Timer, save_vectors, load_vectors,
    TSNE_FILE, NORMALIZED_FILE,
    NUM_CLUSTERS, RANDOM_SEED, TSNE_COMPONENTS, TSNE_PERPLEXITY
)
from visualization import plot_3d_clusters


def apply_tsne(vectors: np.ndarray, n_components: int = TSNE_COMPONENTS,
               perplexity: int = TSNE_PERPLEXITY, seed: int = RANDOM_SEED) -> np.ndarray:
    """
    Apply t-SNE dimensionality reduction

    Args:
        vectors: Input vectors (N, dim)
        n_components: Number of dimensions to reduce to
        perplexity: t-SNE perplexity parameter
        seed: Random seed

    Returns:
        Transformed vectors (N, n_components)
    """
    print(f"    Original shape: {vectors.shape}")
    print(f"    Target dimensions: {n_components}")
    print(f"    Perplexity: {perplexity}")
    print(f"    Running t-SNE (this may take a while)...")

    tsne = TSNE(
        n_components=n_components,
        perplexity=perplexity,
        random_state=seed,
        max_iter=1000,
        learning_rate=200.0,
        verbose=0
    )

    transformed = tsne.fit_transform(vectors)

    print(f"    ✓ t-SNE complete")
    print(f"    Transformed shape: {transformed.shape}")
    print(f"    KL divergence: {tsne.kl_divergence_:.4f}")

    return transformed


def apply_kmeans(vectors: np.ndarray, k: int = NUM_CLUSTERS,
                 seed: int = RANDOM_SEED) -> np.ndarray:
    """
    Apply K-means clustering

    Args:
        vectors: Input vectors (N, dim)
        k: Number of clusters
        seed: Random seed

    Returns:
        Array of cluster labels
    """
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(vectors)

    # Print cluster distribution
    unique, counts = np.unique(labels, return_counts=True)
    print(f"    Number of clusters: {k}")
    for cluster_id, count in zip(unique, counts):
        print(f"      Cluster {cluster_id}: {count} points")

    # Print inertia
    print(f"    Inertia: {kmeans.inertia_:.4f}")

    return labels


def tsne_pipeline(vectors: np.ndarray) -> dict:
    """
    Execute t-SNE pipeline with timing

    Args:
        vectors: Input vectors (N, dim)

    Returns:
        Dictionary with results
    """
    print("=" * 60)
    print("TASK 5: t-SNE Implementation")
    print("=" * 60)
    print(f"\nInput: {vectors.shape[0]} vectors × {vectors.shape[1]} dimensions")
    print(f"Target: Reduce to {TSNE_COMPONENTS} dimensions using t-SNE")
    print(f"Note: t-SNE is computationally intensive and may take longer\n")

    results = {}

    # Apply t-SNE
    with Timer("Apply t-SNE transformation"):
        vectors_3d = apply_tsne(
            vectors,
            n_components=TSNE_COMPONENTS,
            perplexity=TSNE_PERPLEXITY
        )
        results['vectors_3d'] = vectors_3d

    # Apply K-means
    with Timer("Apply K-means clustering"):
        labels = apply_kmeans(vectors_3d, k=NUM_CLUSTERS)
        results['labels'] = labels

    # Visualize
    with Timer("Create 3D visualization"):
        sentence_ids = np.arange(len(vectors_3d))
        print(f"    Generating 3D scatter plot...")
        plot_3d_clusters(
            vectors_3d,
            labels,
            "t-SNE + K-Means Clustering",
            sentence_ids=sentence_ids,
            save_path="tsne_clustering.png",
            show=True
        )
        print(f"    ✓ Visualization complete")

    # Save results
    print(f"\nSaving transformed vectors to {TSNE_FILE}...")
    save_vectors(vectors_3d, TSNE_FILE)
    print(f"✓ Transformed vectors saved successfully")

    # Summary
    print(f"\n{'─' * 60}")
    print(f"Summary:")
    print(f"  Method: t-SNE")
    print(f"  Input dimensions: {vectors.shape[1]}")
    print(f"  Output dimensions: {vectors_3d.shape[1]}")
    print(f"  Perplexity: {TSNE_PERPLEXITY}")
    print(f"  Clusters: {NUM_CLUSTERS}")
    print(f"{'─' * 60}")

    return results


def main():
    """Main execution for Task 5"""
    print("\nLoading normalized vectors...")
    vectors = load_vectors(NORMALIZED_FILE)
    print(f"✓ Loaded {vectors.shape[0]} vectors")

    results = tsne_pipeline(vectors)
    return results


if __name__ == "__main__":
    main()
