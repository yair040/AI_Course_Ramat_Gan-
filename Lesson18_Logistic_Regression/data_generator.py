"""
Data Generator Module for Logistic Regression Project

This module generates synthetic datasets for binary classification.
Creates two distinct classes with specified feature distributions.

Author: Yair Levi
Version: 1.0
"""

import numpy as np
from typing import Tuple


def generate_dataset(
    n_samples_per_class: int = 1000,
    class_0_range: Tuple[float, float] = (0.1, 0.4),
    class_1_range: Tuple[float, float] = (0.6, 0.9),
    random_seed: int = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic dataset for binary classification.

    Creates two classes with features uniformly distributed in specified ranges.

    Args:
        n_samples_per_class: Number of samples per class (default: 1000)
        class_0_range: (min, max) range for class 0 features (default: (0.1, 0.4))
        class_1_range: (min, max) range for class 1 features (default: (0.6, 0.9))
        random_seed: Random seed for reproducibility (default: None)

    Returns:
        Tuple containing:
            - X: Feature matrix of shape (n_total_samples, 3)
                 Column 0: Bias term (all ones)
                 Column 1: Feature x1
                 Column 2: Feature x2
            - y: Label vector of shape (n_total_samples,)
                 Values: 0 for class 0, 1 for class 1

    Example:
        >>> X, y = generate_dataset(n_samples_per_class=1000)
        >>> X.shape
        (2000, 3)
        >>> y.shape
        (2000,)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Validate inputs
    if n_samples_per_class <= 0:
        raise ValueError("n_samples_per_class must be positive")

    if class_0_range[0] >= class_0_range[1]:
        raise ValueError("class_0_range must be (min, max) with min < max")

    if class_1_range[0] >= class_1_range[1]:
        raise ValueError("class_1_range must be (min, max) with min < max")

    # Generate Class 0 data
    class_0_x1 = np.random.uniform(
        low=class_0_range[0],
        high=class_0_range[1],
        size=n_samples_per_class
    )
    class_0_x2 = np.random.uniform(
        low=class_0_range[0],
        high=class_0_range[1],
        size=n_samples_per_class
    )

    # Generate Class 1 data
    class_1_x1 = np.random.uniform(
        low=class_1_range[0],
        high=class_1_range[1],
        size=n_samples_per_class
    )
    class_1_x2 = np.random.uniform(
        low=class_1_range[0],
        high=class_1_range[1],
        size=n_samples_per_class
    )

    # Combine features
    x1 = np.concatenate([class_0_x1, class_1_x1])
    x2 = np.concatenate([class_0_x2, class_1_x2])

    # Create bias column (all ones)
    n_total_samples = 2 * n_samples_per_class
    x0 = np.ones(n_total_samples)

    # Stack into feature matrix [x0, x1, x2]
    X = np.column_stack([x0, x1, x2])

    # Create labels (0 for first half, 1 for second half)
    y = np.concatenate([
        np.zeros(n_samples_per_class),
        np.ones(n_samples_per_class)
    ])

    return X, y


def shuffle_dataset(X: np.ndarray, y: np.ndarray, random_seed: int = None) -> Tuple[np.ndarray, np.ndarray]:
    """
    Shuffle dataset while maintaining X-y correspondence.

    Args:
        X: Feature matrix of shape (n_samples, n_features)
        y: Label vector of shape (n_samples,)
        random_seed: Random seed for reproducibility (default: None)

    Returns:
        Tuple containing shuffled (X, y)

    Example:
        >>> X_shuffled, y_shuffled = shuffle_dataset(X, y, random_seed=42)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    n_samples = X.shape[0]

    # Generate random permutation
    indices = np.random.permutation(n_samples)

    # Apply permutation
    X_shuffled = X[indices]
    y_shuffled = y[indices]

    return X_shuffled, y_shuffled


def validate_dataset(X: np.ndarray, y: np.ndarray) -> bool:
    """
    Validate dataset structure and properties.

    Args:
        X: Feature matrix
        y: Label vector

    Returns:
        True if dataset is valid, raises exception otherwise

    Raises:
        ValueError: If dataset structure is invalid
    """
    # Check dimensions
    if X.ndim != 2:
        raise ValueError(f"X must be 2D array, got {X.ndim}D")

    if y.ndim != 1:
        raise ValueError(f"y must be 1D array, got {y.ndim}D")

    # Check matching samples
    if X.shape[0] != y.shape[0]:
        raise ValueError(
            f"X and y must have same number of samples. "
            f"Got X: {X.shape[0]}, y: {y.shape[0]}"
        )

    # Check feature count
    if X.shape[1] != 3:
        raise ValueError(f"X must have 3 features, got {X.shape[1]}")

    # Check bias column (first column should be all ones)
    if not np.allclose(X[:, 0], 1.0):
        raise ValueError("First column of X (x0) must be all ones (bias term)")

    # Check labels are binary
    unique_labels = np.unique(y)
    if not np.array_equal(unique_labels, np.array([0, 1])):
        raise ValueError(f"Labels must be binary (0 and 1), got {unique_labels}")

    return True
