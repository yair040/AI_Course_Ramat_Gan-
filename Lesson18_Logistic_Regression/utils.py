"""
Utility Functions Module for Logistic Regression Project

This module provides helper functions for error calculations,
metrics computation, and general utilities.

Author: Yair Levi
Version: 1.0
"""

import numpy as np
from typing import Tuple, Dict


def calculate_squared_errors(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Calculate squared errors for each sample.

    Args:
        y_true: True labels, shape (n_samples,)
        y_pred: Predicted probabilities, shape (n_samples,)

    Returns:
        Squared errors array, shape (n_samples,)

    Example:
        >>> y_true = np.array([0, 1, 1, 0])
        >>> y_pred = np.array([0.1, 0.9, 0.7, 0.2])
        >>> errors = calculate_squared_errors(y_true, y_pred)
    """
    return (y_true - y_pred) ** 2


def calculate_average_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calculate average squared error.

    Formula: Σ(y - p)² / (n - 1)
    Uses Bessel's correction (n-1) for unbiased variance estimate.

    Args:
        y_true: True labels, shape (n_samples,)
        y_pred: Predicted probabilities, shape (n_samples,)

    Returns:
        Average squared error (float)

    Example:
        >>> avg_error = calculate_average_error(y_true, y_pred)
    """
    n = len(y_true)
    if n <= 1:
        raise ValueError("Need at least 2 samples to calculate average error")

    squared_errors = calculate_squared_errors(y_true, y_pred)
    return np.sum(squared_errors) / (n - 1)


def calculate_log_likelihood(y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-15) -> float:
    """
    Calculate log-likelihood for binary classification.

    Formula: Σ[y*log(p) + (1-y)*log(1-p)]

    Args:
        y_true: True labels, shape (n_samples,)
        y_pred: Predicted probabilities, shape (n_samples,)
        epsilon: Small value to prevent log(0) (default: 1e-15)

    Returns:
        Log-likelihood value (float)

    Example:
        >>> ll = calculate_log_likelihood(y_true, y_pred)
    """
    # Clip predictions to avoid log(0)
    y_pred_clipped = np.clip(y_pred, epsilon, 1 - epsilon)

    # Calculate log-likelihood
    log_likelihood = np.sum(
        y_true * np.log(y_pred_clipped) +
        (1 - y_true) * np.log(1 - y_pred_clipped)
    )

    return log_likelihood


def calculate_accuracy(y_true: np.ndarray, y_pred: np.ndarray, threshold: float = 0.5) -> float:
    """
    Calculate classification accuracy.

    Args:
        y_true: True labels, shape (n_samples,)
        y_pred: Predicted probabilities, shape (n_samples,)
        threshold: Decision threshold (default: 0.5)

    Returns:
        Accuracy as percentage (0-100)

    Example:
        >>> accuracy = calculate_accuracy(y_true, y_pred)
        >>> print(f"Accuracy: {accuracy:.2f}%")
    """
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred >= threshold).astype(int)

    # Calculate accuracy
    correct = np.sum(y_true == y_pred_binary)
    total = len(y_true)

    return (correct / total) * 100.0


def get_misclassified_indices(y_true: np.ndarray, y_pred: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Get indices of misclassified samples.

    Args:
        y_true: True labels, shape (n_samples,)
        y_pred: Predicted probabilities, shape (n_samples,)
        threshold: Decision threshold (default: 0.5)

    Returns:
        Array of indices where predictions are incorrect

    Example:
        >>> misclassified = get_misclassified_indices(y_true, y_pred)
        >>> print(f"Misclassified samples: {len(misclassified)}")
    """
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred >= threshold).astype(int)

    # Find misclassified indices
    misclassified = np.where(y_true != y_pred_binary)[0]

    return misclassified


def calculate_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, threshold: float = 0.5) -> Dict[str, int]:
    """
    Calculate confusion matrix components.

    Args:
        y_true: True labels, shape (n_samples,)
        y_pred: Predicted probabilities, shape (n_samples,)
        threshold: Decision threshold (default: 0.5)

    Returns:
        Dictionary with keys: 'TP', 'TN', 'FP', 'FN'

    Example:
        >>> cm = calculate_confusion_matrix(y_true, y_pred)
        >>> print(f"True Positives: {cm['TP']}")
    """
    # Convert probabilities to binary predictions
    y_pred_binary = (y_pred >= threshold).astype(int)

    # Calculate confusion matrix components
    tp = np.sum((y_true == 1) & (y_pred_binary == 1))
    tn = np.sum((y_true == 0) & (y_pred_binary == 0))
    fp = np.sum((y_true == 0) & (y_pred_binary == 1))
    fn = np.sum((y_true == 1) & (y_pred_binary == 0))

    return {
        'TP': int(tp),
        'TN': int(tn),
        'FP': int(fp),
        'FN': int(fn)
    }


def format_equation(coefficients: np.ndarray, precision: int = 6) -> str:
    """
    Format the sigmoid equation with actual coefficient values.

    Args:
        coefficients: Array of [β₀, β₁, β₂]
        precision: Number of decimal places (default: 6)

    Returns:
        Formatted equation string

    Example:
        >>> eq = format_equation(np.array([1.5, -2.3, 3.7]))
        >>> print(eq)
        p(x) = 1 / (1 + e^(-(1.500000 + -2.300000*x₁ + 3.700000*x₂)))
    """
    beta_0, beta_1, beta_2 = coefficients

    equation = (
        f"p(x) = 1 / (1 + e^(-({beta_0:.{precision}f} + "
        f"{beta_1:.{precision}f}*x₁ + {beta_2:.{precision}f}*x₂)))"
    )

    return equation


def print_statistics(y_true: np.ndarray, y_pred: np.ndarray, coefficients: np.ndarray) -> None:
    """
    Print comprehensive statistics about the model performance.

    Args:
        y_true: True labels
        y_pred: Predicted probabilities
        coefficients: Model coefficients [β₀, β₁, β₂]

    Example:
        >>> print_statistics(y_true, y_pred, coefficients)
    """
    # Calculate metrics
    accuracy = calculate_accuracy(y_true, y_pred)
    avg_error = calculate_average_error(y_true, y_pred)
    log_likelihood = calculate_log_likelihood(y_true, y_pred)
    cm = calculate_confusion_matrix(y_true, y_pred)
    misclassified = get_misclassified_indices(y_true, y_pred)

    # Print results
    print("\n" + "=" * 60)
    print("MODEL TRAINING RESULTS")
    print("=" * 60)

    print("\nFinal Sigmoid Equation:")
    print(format_equation(coefficients))

    print(f"\nModel Coefficients:")
    print(f"  β₀ (intercept): {coefficients[0]:.6f}")
    print(f"  β₁ (weight x₁): {coefficients[1]:.6f}")
    print(f"  β₂ (weight x₂): {coefficients[2]:.6f}")

    print(f"\nPerformance Metrics:")
    print(f"  Accuracy: {accuracy:.2f}%")
    print(f"  Average Squared Error: {avg_error:.6f}")
    print(f"  Log-Likelihood: {log_likelihood:.2f}")

    print(f"\nConfusion Matrix:")
    print(f"  True Positives:  {cm['TP']:4d}")
    print(f"  True Negatives:  {cm['TN']:4d}")
    print(f"  False Positives: {cm['FP']:4d}")
    print(f"  False Negatives: {cm['FN']:4d}")

    print(f"\nMisclassified Samples: {len(misclassified)}")
    print("=" * 60 + "\n")
