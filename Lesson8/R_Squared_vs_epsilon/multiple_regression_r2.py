#!/usr/bin/env python3
"""
Multiple Linear Regression R² Analysis with Fixed Noise Values

This program demonstrates how R² (coefficient of determination) changes
as we add different fixed noise values to a multiple linear regression model.

Model: Y = β₀ + β₁*x₁ + β₂*x₂ + ... + β₅₀*x₅₀ + ε

Where ε is a fixed noise value uniformly distributed between -1 and 1.

The program uses DOT PRODUCT operations for all calculations.

Author: Yair Levi
Version: 1.0
Python: 3.6+
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# CONFIGURATION PARAMETERS
# =============================================================================

NUM_PREDICTORS = 50      # Number of independent x variables (x1, x2, ..., x50)
NUM_DEPENDENT_PREDICTORS = 5  # Number of dependent predictors to add
NUM_SAMPLES = 100        # Number of data points to generate
NUM_EPSILON_VALUES = 20  # Number of different epsilon (noise) values to test

# Beta coefficient ranges
BETA_0_MIN = -0.5
BETA_0_MAX = 0.5
BETA_I_MIN = -0.9
BETA_I_MAX = 0.9

# X distribution parameters
MU_X = 0                 # Mean of X distribution
SIGMA_X = 1              # Standard deviation of X distribution

# Epsilon (noise) range - the actual noise values (uniform distribution)
EPSILON_MIN = -3.5
EPSILON_MAX = 3.5

SEED = 42                # Random seed for reproducibility

# =============================================================================
# STEP 1-4: GENERATE COEFFICIENTS
# =============================================================================

def generate_coefficients(num_predictors, beta_0_range, beta_i_range, seed=None):
    """
    Generate random coefficients for the regression model.
    
    Args:
        num_predictors (int): Number of predictors (50)
        beta_0_range (tuple): (min, max) for intercept
        beta_i_range (tuple): (min, max) for other coefficients
        seed (int, optional): Random seed
    
    Returns:
        np.ndarray: Array of coefficients [β₀, β₁, β₂, ..., β₅₀]
    """
    if seed is not None:
        np.random.seed(seed)
    
    # Step 3: Choose β₀ randomly between -0.5 and 0.5
    beta_0 = np.random.uniform(beta_0_range[0], beta_0_range[1])
    
    # Step 4: Choose each βᵢ randomly between -0.9 and 0.9
    beta_i = np.random.uniform(beta_i_range[0], beta_i_range[1], num_predictors)
    
    # Combine into single array: [β₀, β₁, β₂, ..., β₅₀]
    coefficients = np.concatenate([[beta_0], beta_i])
    
    return coefficients


# =============================================================================
# STEP 5-6: GENERATE X DATA
# =============================================================================

def generate_x_data(num_samples, num_predictors, mu, sigma, seed=None):
    """
    Generate random X data matrix from normal distribution.
    
    Args:
        num_samples (int): Number of observations (rows)
        num_predictors (int): Number of predictors (columns)
        mu (float): Mean of normal distribution
        sigma (float): Standard deviation of normal distribution
        seed (int, optional): Random seed
    
    Returns:
        np.ndarray: X matrix of shape (num_samples, num_predictors)
    """
    if seed is not None:
        np.random.seed(seed + 1)  # Different seed for X
    
    # Step 5-6: Generate 50 predictors from Normal(μ=0, σ=1)
    # Each column is one predictor variable
    X = np.random.normal(mu, sigma, (num_samples, num_predictors))
    
    return X


# =============================================================================
# STEP 7: GENERATE EPSILON VALUES
# =============================================================================

def generate_epsilon_values(num_epsilon, epsilon_min, epsilon_max):
    """
    Create vector of epsilon (noise) values.
    
    These are the ACTUAL NOISE VALUES (not standard deviations).
    They are uniformly distributed between -1 and 1.
    
    Args:
        num_epsilon (int): Number of epsilon values (20)
        epsilon_min (float): Minimum epsilon value (-1)
        epsilon_max (float): Maximum epsilon value (1)
    
    Returns:
        np.ndarray: Array of 20 epsilon values uniformly distributed [-1, 1]
    """
    # Step 7: Create vector of 20 epsilon (noise) values uniformly distributed
    epsilon_values = np.linspace(epsilon_min, epsilon_max, num_epsilon)
    
    return epsilon_values


# =============================================================================
# ADD DEPENDENT PREDICTORS
# =============================================================================

def add_dependent_predictors(X, num_dependent, seed=None):
    """
    Add dependent predictors that are linear combinations of existing predictors.
    
    These predictors create multicollinearity, which affects model performance.
    
    Args:
        X (np.ndarray): Original predictor matrix, shape (n_samples, n_predictors)
        num_dependent (int): Number of dependent predictors to add
        seed (int, optional): Random seed for reproducibility
    
    Returns:
        np.ndarray: Extended X matrix with dependent predictors added
    """
    if seed is not None:
        np.random.seed(seed + 10)
    
    n_samples, n_predictors = X.shape
    
    # Create dependent predictors as linear combinations
    # Each dependent predictor is a weighted sum of 2-3 original predictors
    dependent_predictors = np.zeros((n_samples, num_dependent))
    
    for i in range(num_dependent):
        # Randomly select 2-3 predictors to combine
        num_to_combine = np.random.randint(2, 4)
        selected_indices = np.random.choice(n_predictors, num_to_combine, replace=False)
        
        # Random weights for combination
        weights = np.random.uniform(-1, 1, num_to_combine)
        
        # Create dependent predictor as weighted sum
        for j, idx in enumerate(selected_indices):
            dependent_predictors[:, i] += weights[j] * X[:, idx]
        
        # Add small noise to make it not perfectly collinear
        noise = np.random.normal(0, 0.1, n_samples)
        dependent_predictors[:, i] += noise
    
    # Concatenate original and dependent predictors
    X_extended = np.hstack([X, dependent_predictors])
    
    return X_extended

def calculate_y_with_fixed_epsilon(X, coefficients, epsilon_value):
    """
    Calculate Y using the multiple linear regression equation with FIXED EPSILON.
    
    Model: Y = β₀ + β₁*x₁ + β₂*x₂ + ... + β₅₀*x₅₀ + ε
    
    Using dot product:
    Y = X_augmented · β + ε
    
    Where:
    - X_augmented has a column of 1's for the intercept
    - ε is a FIXED VALUE (same for all samples in this calculation)
    
    Args:
        X (np.ndarray): Predictor matrix, shape (n_samples, n_predictors)
        coefficients (np.ndarray): Coefficients [β₀, β₁, ..., β₅₀]
        epsilon_value (float): Fixed epsilon (noise) value
    
    Returns:
        tuple: (Y, Y_linear) where Y includes noise and Y_linear is without noise
    """
    num_samples = X.shape[0]
    
    # Add column of 1's for intercept (augmented design matrix)
    # Shape: (n_samples, 1)
    ones = np.ones((num_samples, 1))
    
    # Augmented X: [1, x₁, x₂, ..., x₅₀]
    # Shape: (n_samples, n_predictors + 1)
    X_augmented = np.hstack([ones, X])
    
    # Calculate linear part using DOT PRODUCT
    # For each sample: y_linear = β₀*1 + β₁*x₁ + β₂*x₂ + ... + β₅₀*x₅₀
    # Matrix multiplication: X_augmented @ coefficients
    # This is equivalent to: dot product of each row with coefficient vector
    Y_linear = np.dot(X_augmented, coefficients)
    
    # Step 8: Add FIXED epsilon to all predictions
    # Same epsilon value added to all samples
    Y = Y_linear + epsilon_value
    
    return Y, Y_linear


# =============================================================================
# STEP 9: CALCULATE R-SQUARED USING DOT PRODUCT
# =============================================================================

def calculate_r_squared(Y_observed, Y_predicted):
    """
    Calculate R² (coefficient of determination) using DOT PRODUCT.
    
    R² = 1 - (SS_res / SS_tot)
    
    Where:
    - SS_res = Σ(yᵢ - ŷᵢ)² = residual sum of squares
    - SS_tot = Σ(yᵢ - ȳ)² = total sum of squares
    
    Using dot product:
    - SS_res = dot(residuals, residuals)
    - SS_tot = dot(deviations, deviations)
    
    Args:
        Y_observed (np.ndarray): Observed Y values (with noise)
        Y_predicted (np.ndarray): Predicted Y values (linear part, no noise)
    
    Returns:
        float: R² value
    """
    # Calculate mean of observed Y
    Y_mean = np.mean(Y_observed)
    
    # Calculate residuals: (yᵢ - ŷᵢ)
    # Difference between observed and predicted
    residuals = Y_observed - Y_predicted
    
    # Calculate deviations from mean: (yᵢ - ȳ)
    deviations = Y_observed - Y_mean
    
    # Calculate SS_res using DOT PRODUCT
    # SS_res = Σ(yᵢ - ŷᵢ)² = dot(residuals, residuals)
    SS_res = np.dot(residuals, residuals)
    
    # Calculate SS_tot using DOT PRODUCT
    # SS_tot = Σ(yᵢ - ȳ)² = dot(deviations, deviations)
    SS_tot = np.dot(deviations, deviations)
    
    # Calculate R²
    # R² = 1 - (SS_res / SS_tot)
    # When epsilon = 0: residuals are small → R² close to 1
    # When epsilon is large: residuals are large → R² decreases
    if SS_tot == 0:
        return 1.0  # Perfect fit if no variance
    
    r_squared = 1 - (SS_res / SS_tot)
    
    return r_squared


def calculate_adjusted_r_squared(Y_observed, Y_predicted, n_samples, n_predictors):
    """
    Calculate Adjusted R² which accounts for number of predictors.
    
    Adjusted R² = 1 - [(1 - R²) * (n - 1) / (n - p - 1)]
    
    Where:
    - n = number of samples
    - p = number of predictors (excluding intercept)
    - R² = regular coefficient of determination
    
    Adjusted R² penalizes for adding predictors that don't improve the model.
    It can be negative if the model is very poor.
    
    Args:
        Y_observed (np.ndarray): Observed Y values
        Y_predicted (np.ndarray): Predicted Y values
        n_samples (int): Number of observations
        n_predictors (int): Number of predictor variables (excluding intercept)
    
    Returns:
        float: Adjusted R² value
    """
    # First calculate regular R²
    r_squared = calculate_r_squared(Y_observed, Y_predicted)
    
    # Calculate Adjusted R²
    # Formula: Adj_R² = 1 - [(1 - R²) * (n - 1) / (n - p - 1)]
    if n_samples <= n_predictors + 1:
        # Not enough samples for adjustment
        return r_squared
    
    adjustment_factor = (n_samples - 1) / (n_samples - n_predictors - 1)
    adjusted_r_squared = 1 - (1 - r_squared) * adjustment_factor
    
    return adjusted_r_squared


# =============================================================================
# STEP 10: VISUALIZATION
# =============================================================================

def plot_r_squared_comparison(epsilon_values, r_squared_original, r_squared_dependent, 
                             adj_r_squared_original, adj_r_squared_dependent):
    """
    Draw graph comparing R² and Adjusted R² for both models.
    
    Args:
        epsilon_values (np.ndarray): Array of fixed epsilon values
        r_squared_original (np.ndarray): R² values for original 50 predictors
        r_squared_dependent (np.ndarray): R² values with 55 predictors
        adj_r_squared_original (np.ndarray): Adjusted R² for original 50 predictors
        adj_r_squared_dependent (np.ndarray): Adjusted R² for 55 predictors
    """
    plt.figure(figsize=(16, 9))
    
    # Plot R² for original predictors (50) - SOLID LINE
    plt.plot(epsilon_values, r_squared_original, 'b-o', linewidth=2.5, 
             markersize=8, markerfacecolor='lightblue', markeredgecolor='navy',
             label='R² - Original (50 predictors)', alpha=0.8)
    
    # Plot R² for model with dependent predictors (55) - SOLID LINE
    plt.plot(epsilon_values, r_squared_dependent, 'g-s', linewidth=2.5,
             markersize=7, markerfacecolor='lightgreen', markeredgecolor='darkgreen',
             label='R² - With multicollinearity (55 predictors)', alpha=0.8)
    
    # Plot Adjusted R² for original predictors (50) - DASHED LINE
    plt.plot(epsilon_values, adj_r_squared_original, 'b--^', linewidth=2, 
             markersize=6, markerfacecolor='cyan', markeredgecolor='navy',
             label='Adj R² - Original (50 predictors)', alpha=0.8)
    
    # Plot Adjusted R² for model with dependent predictors (55) - DASHED LINE
    plt.plot(epsilon_values, adj_r_squared_dependent, 'g--d', linewidth=2,
             markersize=6, markerfacecolor='lime', markeredgecolor='darkgreen',
             label='Adj R² - With multicollinearity (55 predictors)', alpha=0.8)
    
    # Add reference lines
    plt.axhline(y=1.0, color='red', linestyle='--', linewidth=1, 
                alpha=0.4, label='Perfect fit (R²=1)')
    plt.axhline(y=0.5, color='orange', linestyle='--', linewidth=1, 
                alpha=0.3, label='R²=0.5')
    plt.axhline(y=0.0, color='gray', linestyle='--', linewidth=1, 
                alpha=0.3, label='R²=0')
    plt.axvline(x=0.0, color='purple', linestyle=':', linewidth=2,
                alpha=0.5, label='ε=0 (no noise)')
    
    # Labels and title
    plt.xlabel('Epsilon (Fixed Noise Value)', fontsize=14, fontweight='bold')
    plt.ylabel('R² / Adjusted R² (Coefficient of Determination)', fontsize=14, fontweight='bold')
    plt.title('R² and Adjusted R² Comparison: Independent vs Multicollinear Models\n' + 
              'Effect of Dependent Predictors on Model Performance Metrics',
              fontsize=15, fontweight='bold')
    
    # Grid and legend
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10, loc='best', ncol=2)
    
    # Set axis limits
    plt.ylim(-0.1, 1.1)
    plt.xlim(epsilon_values[0] - 0.2, epsilon_values[-1] + 0.2)
    
    # Add annotations showing difference at ε≈0
    zero_idx = np.argmin(np.abs(epsilon_values))
    
    # R² difference
    r2_diff = abs(r_squared_original[zero_idx] - r_squared_dependent[zero_idx])
    # Adjusted R² difference
    adj_r2_diff = abs(adj_r_squared_original[zero_idx] - adj_r_squared_dependent[zero_idx])
    
    # Annotation box for differences
    annotation_text = (
        f'At ε≈0:\n'
        f'R² difference: {r2_diff:.4f}\n'
        f'Adj R² difference: {adj_r2_diff:.4f}\n'
        f'\n'
        f'Original (50p):\n'
        f'  R² = {r_squared_original[zero_idx]:.4f}\n'
        f'  Adj R² = {adj_r_squared_original[zero_idx]:.4f}\n'
        f'\n'
        f'Multicollinear (55p):\n'
        f'  R² = {r_squared_dependent[zero_idx]:.4f}\n'
        f'  Adj R² = {adj_r_squared_dependent[zero_idx]:.4f}'
    )
    
    plt.text(0.02, 0.98, annotation_text,
             transform=plt.gca().transAxes,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8),
             fontsize=9, family='monospace')
    
    # Add explanation text
    explanation_text = (
        'Key Insights:\n'
        '• Solid lines = R²\n'
        '• Dashed lines = Adjusted R²\n'
        '• Adjusted R² penalizes extra predictors\n'
        '• Notice larger gap with multicollinearity'
    )
    
    plt.text(0.98, 0.02, explanation_text,
             transform=plt.gca().transAxes,
             verticalalignment='bottom',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
             fontsize=9)
    
    plt.tight_layout()
    plt.show()


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def print_section_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    """
    Main function to execute the complete R² analysis workflow.
    
    Now includes comparison between:
    1. Original model with 50 independent predictors
    2. Model with 55 predictors (50 + 5 dependent/multicollinear)
    
    IMPORTANT: Y is generated using ALL 55 predictors, then:
    - Original model tries to predict Y using only 50 predictors
    - Extended model predicts Y using all 55 predictors
    This ensures R² for extended model ≥ R² for original model
    """
    # Header
    print("=" * 80)
    print("MULTIPLE LINEAR REGRESSION R² ANALYSIS")
    print("Comparison: Independent vs Multicollinear Predictors")
    print("=" * 80)
    print(f"Author: Yair Levi\n")
    
    # Configuration summary
    print("Configuration:")
    print(f"  Original predictors:         {NUM_PREDICTORS}")
    print(f"  Dependent predictors added:  {NUM_DEPENDENT_PREDICTORS}")
    print(f"  Total with multicollinearity:{NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS}")
    print(f"  Number of samples:           {NUM_SAMPLES}")
    print(f"  Number of epsilon values:    {NUM_EPSILON_VALUES}")
    print(f"  β₀ range:                    [{BETA_0_MIN}, {BETA_0_MAX}]")
    print(f"  βᵢ range:                    [{BETA_I_MIN}, {BETA_I_MAX}]")
    print(f"  X ~ Normal(μ={MU_X}, σ={SIGMA_X})")
    print(f"  Epsilon (noise) range:       [{EPSILON_MIN}, {EPSILON_MAX}]")
    print(f"  Random seed:                 {SEED}")
    
    print("\nData Generation Strategy:")
    print(f"  • Y is generated using ALL {NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS} predictors")
    print(f"  • Original model uses only first {NUM_PREDICTORS} predictors")
    print(f"  • Extended model uses all {NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS} predictors")
    print(f"  • This ensures R² (extended) ≥ R² (original)")
    
    # Step 1-4: Generate coefficients (for original 50 predictors)
    print_section_header("STEP 1-4: GENERATING COEFFICIENTS")
    coefficients_original = generate_coefficients(
        NUM_PREDICTORS, 
        (BETA_0_MIN, BETA_0_MAX),
        (BETA_I_MIN, BETA_I_MAX),
        seed=SEED
    )
    
    print(f"Generated {len(coefficients_original)} coefficients for original model:")
    print(f"  β₀ (intercept):              {coefficients_original[0]:.6f}")
    print(f"  β₁ to β₅₀ (predictors):      min={coefficients_original[1:].min():.6f}, "
          f"max={coefficients_original[1:].max():.6f}")
    
    # Generate additional coefficients for dependent predictors
    np.random.seed(SEED + 50)
    coefficients_dependent = np.random.uniform(BETA_I_MIN, BETA_I_MAX, NUM_DEPENDENT_PREDICTORS)
    coefficients_extended = np.concatenate([coefficients_original, coefficients_dependent])
    
    print(f"\nGenerated {NUM_DEPENDENT_PREDICTORS} additional coefficients for dependent predictors:")
    print(f"  β₅₁ to β₅₅:                  min={coefficients_dependent.min():.6f}, "
          f"max={coefficients_dependent.max():.6f}")
    print(f"\nTotal coefficients for extended model: {len(coefficients_extended)}")
    
    # Step 5-6: Generate X data (original 50 predictors)
    print_section_header("STEP 5-6: GENERATING X DATA")
    X_original = generate_x_data(NUM_SAMPLES, NUM_PREDICTORS, MU_X, SIGMA_X, seed=SEED)
    
    print(f"Generated original X matrix:")
    print(f"  Shape:                       {X_original.shape} (samples × predictors)")
    print(f"  X mean:                      {X_original.mean():.6f}")
    print(f"  X std:                       {X_original.std():.6f}")
    
    # Add dependent predictors
    X_extended = add_dependent_predictors(X_original, NUM_DEPENDENT_PREDICTORS, seed=SEED)
    
    print(f"\nGenerated extended X matrix with dependent predictors:")
    print(f"  Shape:                       {X_extended.shape} (samples × predictors)")
    print(f"  Added {NUM_DEPENDENT_PREDICTORS} dependent predictors (multicollinearity)")
    
    # Step 7: Generate epsilon values
    print_section_header("STEP 7: GENERATING EPSILON (NOISE) VALUES")
    epsilon_values = generate_epsilon_values(NUM_EPSILON_VALUES, EPSILON_MIN, EPSILON_MAX)
    
    print(f"Generated {len(epsilon_values)} epsilon (fixed noise) values:")
    print(f"  Range:                       [{epsilon_values[0]:.4f}, "
          f"{epsilon_values[-1]:.4f}]")
    print(f"  First 5 values:              {epsilon_values[:5]}")
    print(f"  Last 5 values:               {epsilon_values[-5:]}")
    
    # CRITICAL FIX: Generate Y using EXTENDED model (all 55 predictors)
    print_section_header("GENERATING TRUE Y USING EXTENDED MODEL")
    print(f"Calculating true Y using all {NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS} predictors...")
    print(f"Formula: Y_true = β₀ + β₁x₁ + ... + β₅₀x₅₀ + β₅₁x₅₁ + ... + β₅₅x₅₅")
    
    # Calculate base Y_linear using extended model (without epsilon)
    ones = np.ones((NUM_SAMPLES, 1))
    X_extended_augmented = np.hstack([ones, X_extended])
    Y_linear_true = np.dot(X_extended_augmented, coefficients_extended)
    
    print(f"  Y_linear shape:              {Y_linear_true.shape}")
    print(f"  Y_linear mean:               {Y_linear_true.mean():.6f}")
    print(f"  Y_linear std:                {Y_linear_true.std():.6f}")
    
    # Step 8-9: Calculate R² and Adj R² for BOTH MODELS across all epsilon values
    print_section_header("STEP 8-9: CALCULATING METRICS FOR BOTH MODELS")
    print("Processing each epsilon value for both models...")
    
    r_squared_original = np.zeros(NUM_EPSILON_VALUES)
    adj_r_squared_original = np.zeros(NUM_EPSILON_VALUES)
    r_squared_extended = np.zeros(NUM_EPSILON_VALUES)
    adj_r_squared_extended = np.zeros(NUM_EPSILON_VALUES)
    
    # Prepare augmented matrices for predictions
    X_original_augmented = np.hstack([ones, X_original])
    
    for i, epsilon_val in enumerate(epsilon_values):
        # Add epsilon to true Y
        Y_observed = Y_linear_true + epsilon_val
        
        # ORIGINAL MODEL: Predict using only first 50 predictors
        Y_pred_original = np.dot(X_original_augmented, coefficients_original)
        r2_orig = calculate_r_squared(Y_observed, Y_pred_original)
        adj_r2_orig = calculate_adjusted_r_squared(Y_observed, Y_pred_original, 
                                                   NUM_SAMPLES, NUM_PREDICTORS)
        r_squared_original[i] = r2_orig
        adj_r_squared_original[i] = adj_r2_orig
        
        # EXTENDED MODEL: Predict using all 55 predictors
        Y_pred_extended = np.dot(X_extended_augmented, coefficients_extended)
        r2_ext = calculate_r_squared(Y_observed, Y_pred_extended)
        adj_r2_ext = calculate_adjusted_r_squared(Y_observed, Y_pred_extended,
                                                  NUM_SAMPLES, 
                                                  NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS)
        r_squared_extended[i] = r2_ext
        adj_r_squared_extended[i] = adj_r2_ext
    
    print(f"\nOriginal Model (50 predictors) Statistics:")
    print(f"  R² Mean:                     {r_squared_original.mean():.6f}")
    print(f"  R² Min:                      {r_squared_original.min():.6f}")
    print(f"  R² Max:                      {r_squared_original.max():.6f}")
    print(f"  Adj R² Mean:                 {adj_r_squared_original.mean():.6f}")
    print(f"  Adj R² Min:                  {adj_r_squared_original.min():.6f}")
    print(f"  Adj R² Max:                  {adj_r_squared_original.max():.6f}")
    
    print(f"\nExtended Model (55 predictors) Statistics:")
    print(f"  R² Mean:                     {r_squared_extended.mean():.6f}")
    print(f"  R² Min:                      {r_squared_extended.min():.6f}")
    print(f"  R² Max:                      {r_squared_extended.max():.6f}")
    print(f"  Adj R² Mean:                 {adj_r_squared_extended.mean():.6f}")
    print(f"  Adj R² Min:                  {adj_r_squared_extended.min():.6f}")
    print(f"  Adj R² Max:                  {adj_r_squared_extended.max():.6f}")
    
    # Comparison
    print_section_header("COMPARISON ANALYSIS")
    print(f"\nMetric Comparison at ε≈0:")
    zero_idx = np.argmin(np.abs(epsilon_values))
    print(f"  Original Model (50 predictors):")
    print(f"    R²:                        {r_squared_original[zero_idx]:.6f}")
    print(f"    Adjusted R²:               {adj_r_squared_original[zero_idx]:.6f}")
    print(f"    Difference (R² - Adj R²):  {r_squared_original[zero_idx] - adj_r_squared_original[zero_idx]:.6f}")
    
    print(f"\n  Extended Model (55 predictors with multicollinearity):")
    print(f"    R²:                        {r_squared_extended[zero_idx]:.6f}")
    print(f"    Adjusted R²:               {adj_r_squared_extended[zero_idx]:.6f}")
    print(f"    Difference (R² - Adj R²):  {r_squared_extended[zero_idx] - adj_r_squared_extended[zero_idx]:.6f}")
    
    print(f"\n  Between Models:")
    print(f"    R² difference:             {abs(r_squared_original[zero_idx] - r_squared_extended[zero_idx]):.6f}")
    print(f"    Adj R² difference:         {abs(adj_r_squared_original[zero_idx] - adj_r_squared_extended[zero_idx]):.6f}")
    
    # Analysis
    print("\nKey Findings:")
    penalty_original = r_squared_original[zero_idx] - adj_r_squared_original[zero_idx]
    penalty_extended = r_squared_extended[zero_idx] - adj_r_squared_extended[zero_idx]
    
    print(f"  • Adjusted R² penalty for original model: {penalty_original:.6f}")
    print(f"  • Adjusted R² penalty for extended model: {penalty_extended:.6f}")
    
    if penalty_extended > penalty_original:
        print("  • Extended model has LARGER penalty from Adjusted R²")
        print("  • This indicates dependent predictors add complexity without proportional value")
    
    if r_squared_extended[zero_idx] >= r_squared_original[zero_idx]:
        print(f"  • Extended model has higher R² (+{r_squared_extended[zero_idx] - r_squared_original[zero_idx]:.6f})")
        print("  • This is expected: more predictors → higher R² (captures true generating process)")
    
    if adj_r_squared_extended[zero_idx] < adj_r_squared_original[zero_idx]:
        print(f"  • BUT Extended model has LOWER Adjusted R² (-{adj_r_squared_original[zero_idx] - adj_r_squared_extended[zero_idx]:.6f})")
        print("  • Adjusted R² correctly identifies that extra predictors don't justify complexity")
    elif adj_r_squared_extended[zero_idx] > adj_r_squared_original[zero_idx]:
        print(f"  • Extended model has higher Adjusted R² (+{adj_r_squared_extended[zero_idx] - adj_r_squared_original[zero_idx]:.6f})")
        print("  • The R² gain exceeds the penalty for added predictors")
    
    print("\n  • R² alone would suggest extended model is better")
    print("  • Adjusted R² provides more nuanced comparison accounting for complexity")
    print("  • Larger penalty gap demonstrates cost of multicollinearity")
    
    # Step 10: Visualization
    print_section_header("STEP 10: COMPARATIVE VISUALIZATION WITH ADJUSTED R²")
    print("Generating comparison plot with 4 lines...")
    print("\nThe graph shows:")
    print("  • Blue solid (○): R² - Original 50 predictors")
    print("  • Blue dashed (△): Adjusted R² - Original 50 predictors")
    print("  • Green solid (□): R² - 55 predictors with multicollinearity")
    print("  • Green dashed (◇): Adjusted R² - 55 predictors with multicollinearity")
    print("\nExpected pattern:")
    print("  • Green solid ≥ Blue solid (R² increases with predictors)")
    print("  • Larger gap for green lines (bigger penalty with more predictors)")
    print("  • Adjusted R² comparison shows true model quality")
    
    plot_r_squared_comparison(epsilon_values, r_squared_original, r_squared_extended,
                             adj_r_squared_original, adj_r_squared_extended)
    
    # Completion
    print("\n" + "=" * 80)
    print("COMPARATIVE ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nKey takeaways:")
    print(f"  • Y was generated using ALL {NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS} predictors")
    print(f"  • Original model uses only {NUM_PREDICTORS} predictors (misses {NUM_DEPENDENT_PREDICTORS})")
    print(f"  • Extended model uses all {NUM_PREDICTORS + NUM_DEPENDENT_PREDICTORS} predictors")
    print(f"  • R² for extended ≥ R² for original (as expected)")
    print(f"  • Adjusted R² shows penalty for extra complexity")
    print(f"  • Demonstrates why Adjusted R² is better for model comparison")
    print("\nClose the plot window to exit.\n")


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    try:
        # Run main analysis
        main()
        
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
