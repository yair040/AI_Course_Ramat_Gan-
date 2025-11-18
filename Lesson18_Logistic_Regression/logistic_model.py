"""
Logistic Regression Model Module

This module implements logistic regression using gradient descent.
Includes sigmoid function, gradient calculation, and training loop.

Author: Yair Levi
Version: 1.0
"""

import numpy as np
from typing import Tuple, Dict, List
from utils import calculate_log_likelihood, calculate_average_error


def sigmoid(X: np.ndarray, coefficients: np.ndarray) -> np.ndarray:
    """
    Compute sigmoid function for all samples.

    Formula: p(i) = 1 / (1 + e^(-(β₀ + β₁*x₁ + β₂*x₂)))

    Args:
        X: Feature matrix, shape (n_samples, 3)
           Columns: [x₀=1, x₁, x₂]
        coefficients: Model coefficients, shape (3,)
                     [β₀, β₁, β₂]

    Returns:
        Probability vector, shape (n_samples,)
        Values in range [0, 1]

    Example:
        >>> X = np.array([[1, 0.2, 0.3], [1, 0.7, 0.8]])
        >>> beta = np.array([0.5, 1.0, -0.5])
        >>> probs = sigmoid(X, beta)
    """
    # Calculate linear combination: X @ coefficients
    # This computes β₀*x₀ + β₁*x₁ + β₂*x₂ for each sample
    z = X @ coefficients

    # Apply sigmoid function: 1 / (1 + e^(-z))
    # Use np.clip to prevent overflow in exp
    z_clipped = np.clip(z, -500, 500)
    probabilities = 1.0 / (1.0 + np.exp(-z_clipped))

    return probabilities


def calculate_gradient(X: np.ndarray, y: np.ndarray, probabilities: np.ndarray) -> np.ndarray:
    """
    Calculate gradient of log-likelihood.

    Formula: g = X^T(y - p)

    Args:
        X: Feature matrix, shape (n_samples, 3)
        y: True labels, shape (n_samples,)
        probabilities: Predicted probabilities, shape (n_samples,)

    Returns:
        Gradient vector, shape (3,)
        One value for each coefficient [∂L/∂β₀, ∂L/∂β₁, ∂L/∂β₂]

    Example:
        >>> gradient = calculate_gradient(X, y, probabilities)
    """
    # Calculate error vector: (y - p)
    error = y - probabilities

    # Calculate gradient: X^T @ error
    # X^T has shape (3, n_samples)
    # error has shape (n_samples,)
    # Result has shape (3,)
    gradient = X.T @ error

    return gradient


def initialize_coefficients(random_seed: int = None) -> np.ndarray:
    """
    Initialize model coefficients randomly.

    Args:
        random_seed: Random seed for reproducibility (default: None)

    Returns:
        Coefficient array [β₀, β₁, β₂] initialized in range [-1, 1]

    Example:
        >>> beta = initialize_coefficients(random_seed=42)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    # Initialize randomly in range [-1, 1]
    coefficients = np.random.uniform(low=-1.0, high=1.0, size=3)

    return coefficients


def train_logistic_regression(
    X: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.3,
    max_iterations: int = 1000,
    convergence_threshold: float = 1e-6,
    verbose: bool = True,
    random_seed: int = None
) -> Tuple[np.ndarray, Dict[str, List]]:
    """
    Train logistic regression model using gradient descent.

    Algorithm:
        1. Initialize coefficients β randomly
        2. For each iteration:
           a. Compute probabilities p using sigmoid
           b. Calculate error (y - p)
           c. Compute gradient g = X^T(y - p)
           d. Update coefficients: β_new = β_old + η * g
           e. Check convergence
        3. Return final coefficients and training history

    Args:
        X: Feature matrix, shape (n_samples, 3)
        y: Label vector, shape (n_samples,)
        learning_rate: Step size η (default: 0.3)
        max_iterations: Maximum training iterations (default: 1000)
        convergence_threshold: Stop if gradient norm < threshold (default: 1e-6)
        verbose: Print training progress (default: True)
        random_seed: Random seed for reproducibility (default: None)

    Returns:
        Tuple containing:
            - coefficients: Final trained coefficients [β₀, β₁, β₂]
            - history: Dictionary with training metrics:
                * 'iteration': List of iteration numbers
                * 'log_likelihood': List of log-likelihood values
                * 'average_error': List of average error values
                * 'gradient_norm': List of gradient norms

    Example:
        >>> beta, history = train_logistic_regression(X, y)
    """
    # Initialize coefficients
    coefficients = initialize_coefficients(random_seed)

    # Initialize history tracking
    history = {
        'iteration': [],
        'log_likelihood': [],
        'average_error': [],
        'gradient_norm': []
    }

    if verbose:
        print("\n" + "=" * 60)
        print("TRAINING LOGISTIC REGRESSION MODEL")
        print("=" * 60)
        print(f"Learning Rate: {learning_rate}")
        print(f"Max Iterations: {max_iterations}")
        print(f"Convergence Threshold: {convergence_threshold}")
        print(f"Initial Coefficients: {coefficients}")
        print("=" * 60 + "\n")

    # Training loop
    for iteration in range(max_iterations):
        # Step 1: Compute probabilities using sigmoid
        probabilities = sigmoid(X, coefficients)

        # Step 2: Calculate gradient
        gradient = calculate_gradient(X, y, probabilities)

        # Step 3: Calculate gradient norm for convergence check
        gradient_norm = np.linalg.norm(gradient)

        # Step 4: Calculate metrics for tracking
        log_likelihood = calculate_log_likelihood(y, probabilities)
        average_error = calculate_average_error(y, probabilities)

        # Step 5: Store metrics in history
        history['iteration'].append(iteration)
        history['log_likelihood'].append(log_likelihood)
        history['average_error'].append(average_error)
        history['gradient_norm'].append(gradient_norm)

        # Step 6: Print progress (every 100 iterations)
        if verbose and (iteration % 100 == 0 or iteration == max_iterations - 1):
            print(f"Iteration {iteration:4d}: "
                  f"Log-Likelihood = {log_likelihood:10.2f}, "
                  f"Avg Error = {average_error:.6f}, "
                  f"Gradient Norm = {gradient_norm:.6f}")

        # Step 7: Check convergence
        if gradient_norm < convergence_threshold:
            if verbose:
                print(f"\nConverged at iteration {iteration}!")
                print(f"Gradient norm ({gradient_norm:.2e}) < threshold ({convergence_threshold:.2e})")
            break

        # Step 8: Update coefficients using gradient ascent
        # β_new = β_old + η * g
        coefficients = coefficients + learning_rate * gradient

    if verbose:
        print("\n" + "=" * 60)
        print("TRAINING COMPLETED")
        print("=" * 60)
        print(f"Final Coefficients: {coefficients}")
        print(f"Total Iterations: {len(history['iteration'])}")
        print("=" * 60 + "\n")

    return coefficients, history


def predict(X: np.ndarray, coefficients: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Make binary predictions on new data.

    Args:
        X: Feature matrix, shape (n_samples, 3)
        coefficients: Trained coefficients [β₀, β₁, β₂]
        threshold: Decision threshold (default: 0.5)

    Returns:
        Binary predictions, shape (n_samples,)
        Values: 0 or 1

    Example:
        >>> predictions = predict(X, coefficients)
    """
    # Get probabilities
    probabilities = sigmoid(X, coefficients)

    # Convert to binary predictions
    predictions = (probabilities >= threshold).astype(int)

    return predictions
