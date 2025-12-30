"""
Dataset Generator Module

Author: Yair Levi
Date: 2025-12-30

Generates datasets for AND and XOR gates with controlled random noise.
"""

import numpy as np
import logging
from typing import Tuple, Dict

logger = logging.getLogger(__name__)


# Truth tables
TRUTH_TABLES = {
    "and": {
        "inputs": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "outputs": [0, 0, 0, 1]
    },
    "xor": {
        "inputs": [[0, 0], [0, 1], [1, 0], [1, 1]],
        "outputs": [0, 1, 1, 0]
    }
}


def generate_truth_table(gate_type: str) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get the base truth table for a specific gate.

    Args:
        gate_type: Type of gate ("and" or "xor")

    Returns:
        Tuple of (inputs, outputs) as numpy arrays
    """
    gate_type = gate_type.lower()
    if gate_type not in TRUTH_TABLES:
        raise ValueError(f"Unknown gate type: {gate_type}")

    truth_table = TRUTH_TABLES[gate_type]
    inputs = np.array(truth_table["inputs"], dtype=np.float32)
    outputs = np.array(truth_table["outputs"], dtype=np.float32)

    logger.info(f"Generated {gate_type.upper()} truth table: {len(inputs)} base points")
    return inputs, outputs


def add_noise(data: np.ndarray, noise_level: float = 0.15) -> np.ndarray:
    """
    Add symmetric random noise to data.

    Args:
        data: Input data array
        noise_level: Maximum noise amplitude (default: 0.15 for ±15%)

    Returns:
        Data with added noise, clipped to [0, 1]
    """
    noise = np.random.uniform(-noise_level, noise_level, size=data.shape)
    noisy_data = data + noise
    # Clip to valid range [0, 1]
    noisy_data = np.clip(noisy_data, 0.0, 1.0)
    return noisy_data.astype(np.float32)


def create_dataset(
    gate_type: str,
    num_samples: int = 600,
    noise_level: float = 0.15,
    validation_split: float = 0.2,
    random_seed: int = 42
) -> Dict[str, np.ndarray]:
    """
    Create complete dataset with noise for training and validation.

    Args:
        gate_type: Type of gate ("and" or "xor")
        num_samples: Total number of samples (default: 600)
        noise_level: Noise amplitude (default: 0.15)
        validation_split: Fraction for validation (default: 0.2)
        random_seed: Random seed for reproducibility

    Returns:
        Dictionary with keys: X_train, X_val, y_train, y_val
    """
    np.random.seed(random_seed)

    # Get base truth table
    base_inputs, base_outputs = generate_truth_table(gate_type)
    num_base_points = len(base_inputs)

    # Calculate samples per base point
    samples_per_point = num_samples // num_base_points

    # Generate replicated dataset
    X_list = []
    y_list = []

    for i in range(num_base_points):
        # Replicate each point
        replicated_inputs = np.tile(base_inputs[i], (samples_per_point, 1))
        replicated_outputs = np.tile(base_outputs[i], samples_per_point)

        # Add noise
        noisy_inputs = add_noise(replicated_inputs, noise_level)
        noisy_outputs = add_noise(replicated_outputs, noise_level)

        X_list.append(noisy_inputs)
        y_list.append(noisy_outputs)

    # Concatenate all samples
    X = np.vstack(X_list)
    y = np.concatenate(y_list)

    # Shuffle the dataset
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]

    # Split into train and validation
    split_idx = int(len(X) * (1 - validation_split))
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]

    logger.info(
        f"{gate_type.upper()} dataset created: "
        f"{len(X_train)} train, {len(X_val)} val samples"
    )

    return {
        "X_train": X_train,
        "X_val": X_val,
        "y_train": y_train,
        "y_val": y_val
    }
