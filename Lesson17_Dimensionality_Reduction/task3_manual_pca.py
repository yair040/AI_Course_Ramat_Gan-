"""
Task 3: Manual PCA Implementation (NumPy only, no sklearn)
"""

import numpy as np
from sklearn.cluster import KMeans
from utils import Timer, save_vectors, MANUAL_PCA_FILE, NUM_CLUSTERS, RANDOM_SEED
from visualization import plot_3d_clusters


def step_a_calculate_mean(vectors: np.ndarray) -> np.ndarray:
    """Step a: Calculate mean for each feature"""
    mean = np.mean(vectors, axis=0)
    print(f"    Mean vector shape: {mean.shape}")
    return mean


def step_b_center_data(vectors: np.ndarray, mean: np.ndarray) -> np.ndarray:
    """Step b: Center data around zero"""
    centered = vectors - mean
    print(f"    Centered data shape: {centered.shape}")
    print(f"    Centered data mean (should be ~0): {np.abs(centered.mean()):.10f}")
    return centered


def step_c_build_matrix_x(centered_vectors: np.ndarray) -> np.ndarray:
    """Step c: Arrange vectors as columns in matrix X"""
    X = centered_vectors.T  # Transpose so vectors are columns
    print(f"    Matrix X shape: {X.shape}")
    print(f"    (Rows: features, Columns: samples)")
    return X


def step_d_covariance_matrix(X: np.ndarray) -> np.ndarray:
    """Step d: Compute covariance matrix S = (X @ X.T) / (n-1)"""
    n = X.shape[1]  # Number of samples (vectors)
    S = (X @ X.T) / (n - 1)
    print(f"    Covariance matrix shape: {S.shape}")
    print(f"    Number of samples (n): {n}")
    # Verify symmetry
    is_symmetric = np.allclose(S, S.T)
    print(f"    Matrix is symmetric: {is_symmetric}")
    return S


def step_e_calculate_eigenvalues(S: np.ndarray) -> np.ndarray:
    """Step e: Calculate eigenvalues of covariance matrix"""
    eigenvalues, _ = np.linalg.eig(S)
    eigenvalues = eigenvalues.real
    print(f"    Number of eigenvalues: {len(eigenvalues)}")
    print(f"    Top 5 eigenvalues: {eigenvalues[:5]}")
    return eigenvalues


def step_f_calculate_eigenvectors(S: np.ndarray) -> tuple:
    """Step f: Calculate eigenvectors of covariance matrix"""
    eigenvalues, eigenvectors = np.linalg.eig(S)
    eigenvalues = eigenvalues.real
    eigenvectors = eigenvectors.real
    print(f"    Eigenvectors shape: {eigenvectors.shape}")
    return eigenvalues, eigenvectors


def step_g_build_transformation_matrix(eigenvectors: np.ndarray,
                                       eigenvalues: np.ndarray, k: int = 3) -> np.ndarray:
    """Step g: Build transformation matrix P from top k eigenvectors"""
    # Sort by eigenvalue (descending)
    idx = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = eigenvalues[idx]
    sorted_eigenvectors = eigenvectors[:, idx]

    # Take top k
    P = sorted_eigenvectors[:, :k]
    print(f"    Transformation matrix P shape: {P.shape}")
    print(f"    Top {k} eigenvalues: {sorted_eigenvalues[:k]}")

    # Calculate explained variance
    total_variance = np.sum(eigenvalues)
    explained_variance = np.sum(sorted_eigenvalues[:k]) / total_variance
    print(f"    Explained variance ratio: {explained_variance:.4f}")
    return P


def step_h_transpose_p(P: np.ndarray) -> np.ndarray:
    """Step h: Compute transpose of P"""
    P_T = P.T
    print(f"    P^T shape: {P_T.shape}")
    return P_T


def step_i_transform_vectors(vectors: np.ndarray, P_T: np.ndarray,
                             mean: np.ndarray) -> np.ndarray:
    """Step i: Transform vectors to new coordinate system"""
    # Center the original vectors
    centered = vectors - mean
    # Transform: new_vector = P^T @ centered_vector
    transformed = (P_T @ centered.T).T
    print(f"    Transformed vectors shape: {transformed.shape}")
    print(f"    Shape is ({transformed.shape[0]} samples, {transformed.shape[1]} dimensions)")
    return transformed


def step_j_kmeans(vectors_3d: np.ndarray, k: int = NUM_CLUSTERS,
                  seed: int = RANDOM_SEED) -> np.ndarray:
    """Step j: K-means clustering"""
    kmeans = KMeans(n_clusters=k, random_state=seed, n_init=10)
    labels = kmeans.fit_predict(vectors_3d)

    # Print cluster distribution
    unique, counts = np.unique(labels, return_counts=True)
    print(f"    Number of clusters: {k}")
    for cluster_id, count in zip(unique, counts):
        print(f"      Cluster {cluster_id}: {count} points")

    return labels


def step_k_visualize(vectors_3d: np.ndarray, labels: np.ndarray):
    """Step k: Visualize 3D clusters"""
    sentence_ids = np.arange(len(vectors_3d))
    print(f"    Creating 3D visualization...")
    plot_3d_clusters(
        vectors_3d,
        labels,
        "Manual PCA + K-Means Clustering",
        sentence_ids=sentence_ids,
        save_path="pca_manual_clustering.png",
        show=True
    )
    print(f"    ✓ Visualization complete")


def manual_pca_pipeline(vectors: np.ndarray) -> dict:
    """Execute manual PCA pipeline with timing"""
    print("=" * 60)
    print("TASK 3: Manual PCA Implementation (NumPy only)")
    print("=" * 60)
    print(f"\nInput: {vectors.shape[0]} vectors × {vectors.shape[1]} dimensions")
    print(f"Target: Reduce to 3 dimensions\n")

    results = {}

    with Timer("Step a: Calculate mean"):
        mean = step_a_calculate_mean(vectors)
        results['mean'] = mean

    with Timer("Step b: Center data around zero"):
        centered = step_b_center_data(vectors, mean)
        results['centered'] = centered

    with Timer("Step c: Build matrix X (vectors as columns)"):
        X = step_c_build_matrix_x(centered)
        results['X'] = X

    with Timer("Step d: Compute covariance matrix"):
        S = step_d_covariance_matrix(X)
        results['covariance'] = S

    with Timer("Step e: Calculate eigenvalues"):
        eigenvalues = step_e_calculate_eigenvalues(S)
        results['eigenvalues'] = eigenvalues

    with Timer("Step f: Calculate eigenvectors"):
        eigenvalues, eigenvectors = step_f_calculate_eigenvectors(S)
        results['eigenvectors'] = eigenvectors

    with Timer("Step g: Build transformation matrix P (top 3 components)"):
        P = step_g_build_transformation_matrix(eigenvectors, eigenvalues, k=3)
        results['P'] = P

    with Timer("Step h: Compute transpose of P"):
        P_T = step_h_transpose_p(P)
        results['P_T'] = P_T

    with Timer("Step i: Transform vectors to 3D"):
        vectors_3d = step_i_transform_vectors(vectors, P_T, mean)
        results['vectors_3d'] = vectors_3d

    with Timer("Step j: K-means clustering (K=3)"):
        labels = step_j_kmeans(vectors_3d, k=NUM_CLUSTERS)
        results['labels'] = labels

    with Timer("Step k: Visualize 3D clusters"):
        step_k_visualize(vectors_3d, labels)

    # Save results
    print(f"\nSaving transformed vectors to {MANUAL_PCA_FILE}...")
    save_vectors(vectors_3d, MANUAL_PCA_FILE)
    print(f"✓ Transformed vectors saved successfully")

    return results


def main():
    """Main execution for Task 3"""
    from utils import load_vectors, NORMALIZED_FILE

    print("\nLoading normalized vectors...")
    vectors = load_vectors(NORMALIZED_FILE)
    print(f"✓ Loaded {vectors.shape[0]} vectors")

    results = manual_pca_pipeline(vectors)
    return results


if __name__ == "__main__":
    main()
