"""
Main Entry Point for Logistic Regression Project

This module orchestrates the entire workflow:
1. Dataset generation
2. Model training
3. Prediction
4. Visualization and results display

Author: Yair Levi
Version: 1.0
"""

import numpy as np
from data_generator import generate_dataset, shuffle_dataset, validate_dataset
from logistic_model import train_logistic_regression, sigmoid
from utils import print_statistics
from visualization import (
    plot_classification_results,
    plot_training_progress,
    display_results_table,
    show_all_plots
)


def main():
    """
    Main function to run the logistic regression pipeline.

    Workflow:
        1. Generate synthetic dataset
        2. Train logistic regression model
        3. Make predictions
        4. Display statistics
        5. Create visualizations
    """
    print("\n" + "=" * 70)
    print(" " * 15 + "LOGISTIC REGRESSION PROJECT")
    print(" " * 20 + "Gradient Descent Implementation")
    print("=" * 70 + "\n")

    # ========================================================================
    # STEP 1: Generate Dataset
    # ========================================================================
    print("STEP 1: Generating Dataset")
    print("-" * 70)

    # Configuration
    n_samples_per_class = 1000
    class_0_range = (0.1, 0.4)
    class_1_range = (0.6, 0.9)
    random_seed = 42

    # Generate data
    X, y = generate_dataset(
        n_samples_per_class=n_samples_per_class,
        class_0_range=class_0_range,
        class_1_range=class_1_range,
        random_seed=random_seed
    )

    # Shuffle dataset for better training
    X, y = shuffle_dataset(X, y, random_seed=random_seed)

    # Validate dataset
    try:
        validate_dataset(X, y)
        print(f"✓ Dataset generated successfully!")
        print(f"  Total samples: {len(X)}")
        print(f"  Features per sample: {X.shape[1]}")
        print(f"  Class 0 samples: {np.sum(y == 0)}")
        print(f"  Class 1 samples: {np.sum(y == 1)}")
        print(f"  Class 0 range: x₁, x₂ ∈ {class_0_range}")
        print(f"  Class 1 range: x₁, x₂ ∈ {class_1_range}")
    except ValueError as e:
        print(f"✗ Dataset validation failed: {e}")
        return

    print()

    # ========================================================================
    # STEP 2: Train Model
    # ========================================================================
    print("STEP 2: Training Logistic Regression Model")
    print("-" * 70)

    # Training configuration
    learning_rate = 0.3
    max_iterations = 1000
    convergence_threshold = 1e-6

    # Train model
    coefficients, history = train_logistic_regression(
        X=X,
        y=y,
        learning_rate=learning_rate,
        max_iterations=max_iterations,
        convergence_threshold=convergence_threshold,
        verbose=True,
        random_seed=random_seed
    )

    print()

    # ========================================================================
    # STEP 3: Make Predictions
    # ========================================================================
    print("STEP 3: Making Predictions")
    print("-" * 70)

    # Calculate probabilities for all samples
    y_pred_probs = sigmoid(X, coefficients)

    # Convert to binary predictions
    y_pred_binary = (y_pred_probs >= 0.5).astype(int)

    print(f"✓ Predictions completed!")
    print(f"  Samples predicted: {len(y_pred_probs)}")
    print(f"  Predicted as Class 0: {np.sum(y_pred_binary == 0)}")
    print(f"  Predicted as Class 1: {np.sum(y_pred_binary == 1)}")

    print()

    # ========================================================================
    # STEP 4: Display Statistics
    # ========================================================================
    print("STEP 4: Calculating Performance Metrics")
    print("-" * 70)

    # Print comprehensive statistics
    print_statistics(y, y_pred_probs, coefficients)

    # ========================================================================
    # STEP 5: Create Visualizations
    # ========================================================================
    print("STEP 5: Creating Visualizations")
    print("-" * 70)

    print("Creating plots...")

    # Plot 1: Classification Results
    plot_classification_results(X, y, y_pred_probs, coefficients)
    print("  ✓ Classification scatter plot created")

    # Plot 2: Training Progress
    plot_training_progress(history)
    print("  ✓ Training progress plots created")

    print("\nDisplaying matplotlib plots...")
    print("(Close all plot windows to continue)")

    # Show all matplotlib plots
    show_all_plots()

    print("\n✓ Matplotlib plots closed")

    # ========================================================================
    # STEP 6: Display Results Table
    # ========================================================================
    print("\nSTEP 6: Displaying Results Table")
    print("-" * 70)
    print("Opening GUI table with detailed results...")
    print("(Close the table window to exit the program)")

    # Display results in GUI table
    display_results_table(X, y, y_pred_probs, coefficients, max_rows=2000)

    # ========================================================================
    # Program Complete
    # ========================================================================
    print("\n" + "=" * 70)
    print(" " * 25 + "PROGRAM COMPLETED")
    print("=" * 70)
    print("\nThank you for using the Logistic Regression Project!")
    print("All results have been displayed.\n")


if __name__ == "__main__":
    """
    Entry point when running the script directly.
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        print("Exiting gracefully...\n")
    except Exception as e:
        print(f"\n\nERROR: An unexpected error occurred:")
        print(f"{type(e).__name__}: {e}")
        print("\nPlease check your configuration and try again.\n")
        raise
