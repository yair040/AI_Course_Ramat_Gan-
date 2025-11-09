"""
Task 4: PCA using sklearn library
"""

import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from utils import (
    Timer, save_vectors, load_vectors,
    SKLEARN_PCA_FILE, NORMALIZED_FILE,
    NUM_CLUSTERS, RANDOM_SEED, PCA_COMPONENTS
)
from visualization import plot_3d_clusters


def apply_pca(vectors: np.ndarray, n_components: int = PCA_COMPONENTS) -> tuple:
    """
    Apply sklearn PCA

    Args:
        vectors: Input vectors (N, dim)
        n_components: Number of principal components

    Returns:
        Tuple of (transformed_vectors, pca_model)
    """
    pca = PCA(n_components=n_components)
    transformed = pca.fit_transform(vectors)

    print(f"    Original shape: {vectors.shape}")
    print(f"    Transformed shape: {transformed.shape}")
    print(f"    Number of components: {n_components}")

    return transformed, pca


def print_pca_statistics(pca: PCA):
    """
    Print detailed PCA statistics

    Args:
        pca: Fitted PCA model
    """
    print(f"\n  PCA Statistics:")
    print(f"    Explained variance ratio per component:")
    for i, var_ratio in enumerate(pca.explained_variance_ratio_, 1):
        print(f"      Component {i}: {var_ratio:.4f} ({var_ratio*100:.2f}%)")

    total_variance = pca.explained_variance_ratio_.sum()
    print(f"    Total explained variance: {total_variance:.4f} ({total_variance*100:.2f}%)")

    print(f"\n    Singular values: {pca.singular_values_[:3]}")


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

    # Print inertia (within-cluster sum of squares)
    print(f"    Inertia: {kmeans.inertia_:.4f}")

    return labels


def sklearn_pca_pipeline(vectors: np.ndarray) -> dict:
    """
    Execute sklearn PCA pipeline with timing

    Args:
        vectors: Input vectors (N, dim)

    Returns:
        Dictionary with results
    """
    print("=" * 60)
    print("TASK 4: sklearn PCA Implementation")
    print("=" * 60)
    print(f"\nInput: {vectors.shape[0]} vectors × {vectors.shape[1]} dimensions")
    print(f"Target: Reduce to {PCA_COMPONENTS} dimensions using sklearn\n")

    results = {}

    # Apply PCA
    with Timer("Apply PCA transformation"):
        vectors_3d, pca = apply_pca(vectors, n_components=PCA_COMPONENTS)
        results['vectors_3d'] = vectors_3d
        results['pca'] = pca

    # Print statistics
    print_pca_statistics(pca)

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
            "sklearn PCA + K-Means Clustering",
            sentence_ids=sentence_ids,
            save_path="pca_sklearn_clustering.png",
            show=True
        )
        print(f"    ✓ Visualization complete")

    # Save results
    print(f"\nSaving transformed vectors to {SKLEARN_PCA_FILE}...")
    save_vectors(vectors_3d, SKLEARN_PCA_FILE)
    print(f"✓ Transformed vectors saved successfully")

    # Summary
    print(f"\n{'─' * 60}")
    print(f"Summary:")
    print(f"  Method: sklearn PCA")
    print(f"  Input dimensions: {vectors.shape[1]}")
    print(f"  Output dimensions: {vectors_3d.shape[1]}")
    print(f"  Variance explained: {pca.explained_variance_ratio_.sum()*100:.2f}%")
    print(f"  Clusters: {NUM_CLUSTERS}")
    print(f"{'─' * 60}")

    return results


def main():
    """Main execution for Task 4"""
    print("\nLoading normalized vectors...")
    vectors = load_vectors(NORMALIZED_FILE)
    print(f"✓ Loaded {vectors.shape[0]} vectors")

    results = sklearn_pca_pipeline(vectors)
    return results


if __name__ == "__main__":
    main()
