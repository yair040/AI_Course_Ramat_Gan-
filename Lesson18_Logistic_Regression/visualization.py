"""
Visualization Module for Logistic Regression Project
Handles plotting and GUI display for classification results.
Author: Yair Levi, Version: 1.0
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List
import tkinter as tk
from tkinter import ttk
from utils import get_misclassified_indices, calculate_squared_errors


def plot_classification_results(X: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray,
                                coefficients: np.ndarray, threshold: float = 0.5) -> None:
    """Create scatter plot of classification results with misclassifications."""
    x1, x2 = X[:, 1], X[:, 2]
    y_pred_binary = (y_pred >= threshold).astype(int)
    misclassified = get_misclassified_indices(y_true, y_pred, threshold)

    plt.figure(figsize=(10, 8))

    # Plot correctly classified samples
    class_0_correct = (y_true == 0) & (y_pred_binary == 0)
    plt.scatter(x1[class_0_correct], x2[class_0_correct],
                c='blue', marker='o', s=30, alpha=0.6, label='Class 0 (Correct)')

    class_1_correct = (y_true == 1) & (y_pred_binary == 1)
    plt.scatter(x1[class_1_correct], x2[class_1_correct],
                c='green', marker='o', s=30, alpha=0.6, label='Class 1 (Correct)')

    # Plot misclassified points
    if len(misclassified) > 0:
        plt.scatter(x1[misclassified], x2[misclassified], c='red', marker='x',
                    s=100, linewidths=2, label=f'Misclassified ({len(misclassified)})')

    # Add decision boundary
    try:
        plot_decision_boundary(coefficients, x1, x2)
    except Exception as e:
        print(f"Warning: Could not plot decision boundary: {e}")

    plt.xlabel('Feature x₁', fontsize=12)
    plt.ylabel('Feature x₂', fontsize=12)
    plt.title('Logistic Regression Classification Results', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()


def plot_decision_boundary(coefficients: np.ndarray, x1: np.ndarray, x2: np.ndarray) -> None:
    """Plot decision boundary line where p(x) = 0.5."""
    beta_0, beta_1, beta_2 = coefficients
    if abs(beta_2) < 1e-10:
        return

    x1_line = np.linspace(x1.min(), x1.max(), 100)
    x2_line = -(beta_0 + beta_1 * x1_line) / beta_2
    plt.plot(x1_line, x2_line, 'k--', linewidth=2, label='Decision Boundary')


def plot_training_progress(history: Dict[str, List]) -> None:
    """Create training progress plots (log-likelihood and average error vs iteration)."""
    iterations = history['iteration']
    log_likelihoods = history['log_likelihood']
    avg_errors = history['average_error']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Log-Likelihood vs Iteration
    ax1.plot(iterations, log_likelihoods, 'b-', linewidth=2)
    ax1.set_xlabel('Iteration', fontsize=12)
    ax1.set_ylabel('Log-Likelihood', fontsize=12)
    ax1.set_title('Log-Likelihood vs Iteration', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Plot 2: Average Error vs Iteration
    ax2.plot(iterations, avg_errors, 'r-', linewidth=2)
    ax2.set_xlabel('Iteration', fontsize=12)
    ax2.set_ylabel('Average Squared Error', fontsize=12)
    ax2.set_title('Average Error vs Iteration', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()


def display_results_table(X: np.ndarray, y_true: np.ndarray, y_pred: np.ndarray,
                         coefficients: np.ndarray, max_rows: int = 100) -> None:
    """Display results in a GUI table using tkinter."""
    y_pred_binary = (y_pred >= 0.5).astype(int)
    squared_errors = calculate_squared_errors(y_true, y_pred)

    # Create main window
    root = tk.Tk()
    root.title("Logistic Regression Results")
    root.geometry("900x600")

    # Add title
    tk.Label(root, text="Logistic Regression Results Table",
             font=("Arial", 14, "bold"), pady=10).pack()

    # Add equation
    from utils import format_equation
    tk.Label(root, text=format_equation(coefficients, precision=6),
             font=("Courier", 10), pady=5).pack()

    # Create frame for table
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create scrollbars and treeview
    vsb = ttk.Scrollbar(frame, orient="vertical")
    hsb = ttk.Scrollbar(frame, orient="horizontal")

    tree = ttk.Treeview(frame,
                        columns=("Index", "x0", "x1", "x2", "y_true", "prob", "pred", "error"),
                        show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    # Define columns
    columns = [
        ("Index", 60), ("x0", 80), ("x1", 100), ("x2", 100),
        ("y_true", 90), ("prob", 110), ("pred", 90), ("error", 120)
    ]
    headers = ["Index", "x₀ (Bias)", "x₁", "x₂", "True Label",
               "Probability", "Prediction", "Squared Error"]

    for (col, width), header in zip(columns, headers):
        tree.heading(col, text=header)
        tree.column(col, width=width, anchor="center")

    # Insert data
    n_samples = min(len(X), max_rows)
    for i in range(n_samples):
        tree.insert("", "end", values=(
            i, f"{X[i, 0]:.0f}", f"{X[i, 1]:.4f}", f"{X[i, 2]:.4f}",
            int(y_true[i]), f"{y_pred[i]:.6f}",
            int(y_pred_binary[i]), f"{squared_errors[i]:.6f}"
        ))

    # Add truncation note
    if len(X) > max_rows:
        tk.Label(root, text=f"Showing first {max_rows} of {len(X)} samples",
                 font=("Arial", 9), fg="red").pack()

    # Layout
    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Close button
    tk.Button(root, text="Close", command=root.destroy, pady=5).pack()
    root.mainloop()


def show_all_plots() -> None:
    """Display all matplotlib plots."""
    plt.show()
