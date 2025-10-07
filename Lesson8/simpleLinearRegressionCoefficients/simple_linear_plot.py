#!/usr/bin/env python3
"""
Linear Regression Data Generator with Coefficient Estimation

Generates random points following Y = β₀ + β₁*X + ε
Then estimates the coefficients using least squares formulas.

Author: Yair Levi
Version: 1.0
Python: 3.6+
"""

import numpy as np
import matplotlib.pyplot as plt

# Configuration parameters
NUM_POINTS = 1000        # Number of data points to generate
MU_X = 0                 # Mean of X distribution
SIGMA_X = 1              # Standard deviation of X distribution
BETA_0 = 0.2             # True intercept parameter
BETA_1 = 0.9             # True slope parameter
EPSILON_SIGMA = 0.3      # Standard deviation of noise (epsilon)
SEED = None              # Random seed for reproducibility (set to int if needed)


def generate_data(n_points, mu_x, sigma_x, beta_0, beta_1, epsilon_sigma, seed=None):
    """
    Generate data following linear model: Y = β₀ + β₁*X + ε
    
    Args:
        n_points (int): Number of points to generate
        mu_x (float): Mean of X distribution
        sigma_x (float): Standard deviation of X distribution
        beta_0 (float): Intercept parameter
        beta_1 (float): Slope parameter
        epsilon_sigma (float): Standard deviation of noise
        seed (int, optional): Random seed for reproducibility
    
    Returns:
        tuple: (X, Y) arrays
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Generate X points from normal distribution
    X = np.random.normal(mu_x, sigma_x, n_points)
    
    # Generate epsilon (noise) from normal distribution
    epsilon = np.random.normal(0, epsilon_sigma, n_points)
    
    # Calculate Y using the equation: Y = β₀ + β₁*X + ε
    Y = beta_0 + beta_1 * X + epsilon
    
    return X, Y


def estimate_coefficients(X, Y):
    """
    Estimate β₀ and β₁ using least squares formulas with dot product.
    
    Formulas:
    β₁ = sum((Xi - X_avg) * (Yi - Y_avg)) / sum((Xi - X_avg)²)
    β₀ = Y_avg - β₁ * X_avg
    
    Args:
        X (np.ndarray): X values
        Y (np.ndarray): Y values
    
    Returns:
        tuple: (beta_0_estimated, beta_1_estimated)
    """
    # Calculate averages using vector operations
    X_avg = np.mean(X)
    Y_avg = np.mean(Y)
    
    # Calculate deviations from mean (vectorized)
    X_dev = X - X_avg  # (Xi - X_avg) for all i
    Y_dev = Y - Y_avg  # (Yi - Y_avg) for all i
    
    # Calculate beta_1 using the formula with DOT PRODUCT
    # β₁ = sum((Xi - X_avg) * (Yi - Y_avg)) / sum((Xi - X_avg)²)
    # Numerator: dot product of X_dev and Y_dev
    numerator = np.dot(X_dev, Y_dev)
    # Denominator: dot product of X_dev with itself
    denominator = np.dot(X_dev, X_dev)
    beta_1_est = numerator / denominator
    
    # Calculate beta_0 using the formula
    # β₀ = Y_avg - β₁ * X_avg
    beta_0_est = Y_avg - beta_1_est * X_avg
    
    return beta_0_est, beta_1_est


def plot_data_and_lines(X, Y, beta_0_true, beta_1_true, beta_0_est, beta_1_est):
    """
    Draw the points, true line, and estimated line in one graph.
    
    Args:
        X (np.ndarray): X values
        Y (np.ndarray): Y values
        beta_0_true (float): True intercept parameter
        beta_1_true (float): True slope parameter
        beta_0_est (float): Estimated intercept parameter
        beta_1_est (float): Estimated slope parameter
    """
    plt.figure(figsize=(12, 8))
    
    # Plot the data points
    plt.scatter(X, Y, alpha=0.4, s=20, c='blue', edgecolors='navy', 
                label=f'Data Points (n={len(X)})')
    
    # Draw the true regression line (without noise)
    x_line = np.linspace(X.min(), X.max(), 100)
    y_true = beta_0_true + beta_1_true * x_line
    plt.plot(x_line, y_true, 'r-', linewidth=3, 
             label=f'True Line: Y = {beta_0_true} + {beta_1_true}*X')
    
    # Draw the estimated regression line
    y_estimated = beta_0_est + beta_1_est * x_line
    plt.plot(x_line, y_estimated, 'g--', linewidth=2.5, 
             label=f'Estimated Line: Y = {beta_0_est:.4f} + {beta_1_est:.4f}*X')
    
    # Add labels and title
    plt.xlabel('X', fontsize=14, fontweight='bold')
    plt.ylabel('Y', fontsize=14, fontweight='bold')
    plt.title('Linear Regression: Data Points with True and Estimated Lines',
              fontsize=15, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11, loc='best')
    
    # Show the plot
    plt.tight_layout()
    plt.show()


def print_results(beta_0_true, beta_1_true, beta_0_est, beta_1_est):
    """
    Print the comparison between true and estimated coefficients.
    
    Args:
        beta_0_true (float): True intercept
        beta_1_true (float): True slope
        beta_0_est (float): Estimated intercept
        beta_1_est (float): Estimated slope
    """
    print("\n" + "=" * 70)
    print("COEFFICIENT ESTIMATION RESULTS")
    print("=" * 70)
    
    print("\nTrue Parameters:")
    print(f"  β₀ (Intercept):           {beta_0_true}")
    print(f"  β₁ (Slope):               {beta_1_true}")
    
    print("\nEstimated Parameters (using vector calculations):")
    print(f"  β₀_est (Intercept):       {beta_0_est:.6f}")
    print(f"  β₁_est (Slope):           {beta_1_est:.6f}")
    
    print("\nEstimation Errors:")
    print(f"  Error in β₀:              {abs(beta_0_est - beta_0_true):.6f}")
    print(f"  Error in β₁:              {abs(beta_1_est - beta_1_true):.6f}")
    print(f"  Relative Error β₀:        {abs(beta_0_est - beta_0_true) / abs(beta_0_true) * 100:.2f}%")
    print(f"  Relative Error β₁:        {abs(beta_1_est - beta_1_true) / abs(beta_1_true) * 100:.2f}%")
    
    print("\n" + "=" * 70)


def main():
    """Main function to run the complete analysis."""
    print("=" * 70)
    print("LINEAR REGRESSION WITH COEFFICIENT ESTIMATION")
    print("=" * 70)
    print(f"Author: Yair Levi\n")
    
    print(f"Configuration:")
    print(f"  Number of Points:    {NUM_POINTS}")
    print(f"  X ~ Normal(μ={MU_X}, σ={SIGMA_X})")
    print(f"  Y = {BETA_0} + {BETA_1}*X + ε")
    print(f"  ε ~ Normal(0, {EPSILON_SIGMA})")
    
    # Step 1: Generate data
    print(f"\n[Step 1] Generating {NUM_POINTS} random points...")
    X, Y = generate_data(NUM_POINTS, MU_X, SIGMA_X, BETA_0, BETA_1, EPSILON_SIGMA, SEED)
    
    print(f"  X range: [{X.min():.3f}, {X.max():.3f}]")
    print(f"  Y range: [{Y.min():.3f}, {Y.max():.3f}]")
    print(f"  X mean: {X.mean():.3f}, X std: {X.std():.3f}")
    print(f"  Y mean: {Y.mean():.3f}, Y std: {Y.std():.3f}")
    
    # Step 2: Estimate coefficients using vector calculations with dot product
    print(f"\n[Step 2] Estimating coefficients using dot product...")
    print(f"  Formula for β₁: dot(Xi - X_avg, Yi - Y_avg) / dot(Xi - X_avg, Xi - X_avg)")
    print(f"  Formula for β₀: Y_avg - β₁ * X_avg")
    
    beta_0_est, beta_1_est = estimate_coefficients(X, Y)
    
    # Print results
    print_results(BETA_0, BETA_1, beta_0_est, beta_1_est)
    
    # Step 3: Plot the data and lines
    print(f"\n[Step 3] Displaying plot with data points and lines...")
    plot_data_and_lines(X, Y, BETA_0, BETA_1, beta_0_est, beta_1_est)
    
    print("\nAnalysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
