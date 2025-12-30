"""
Neural Network Models Module

Author: Yair Levi
Date: 2025-12-30

Defines Keras models for AND and XOR gate implementation.
"""

import logging
from tensorflow import keras
from keras import layers

logger = logging.getLogger(__name__)


def create_and_model() -> keras.Model:
    """
    Create neural network for AND gate (linearly separable).

    Architecture:
        - Input: 2 neurons
        - Output: 1 neuron with sigmoid activation
        - Total parameters: 3 (2 weights + 1 bias)

    Returns:
        Compiled Keras model
    """
    model = keras.Sequential([
        layers.Input(shape=(2,)),
        layers.Dense(1, activation="sigmoid", name="output")
    ], name="AND_Gate")

    # Compile with MSE loss and Adam optimizer
    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["accuracy"]
    )

    logger.info(f"AND model created: {model.count_params()} parameters")
    return model


def create_xor_model() -> keras.Model:
    """
    Create neural network for XOR gate (non-linearly separable).

    Architecture:
        - Input: 2 neurons
        - Hidden: 2 neurons with sigmoid activation
        - Output: 1 neuron with sigmoid activation
        - Total parameters: 9 (2→2: 6 params, 2→1: 3 params)

    Returns:
        Compiled Keras model
    """
    model = keras.Sequential([
        layers.Input(shape=(2,)),
        layers.Dense(2, activation="sigmoid", name="hidden"),
        layers.Dense(1, activation="sigmoid", name="output")
    ], name="XOR_Gate")

    # Compile with MSE loss and Adam optimizer
    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["accuracy"]
    )

    logger.info(f"XOR model created: {model.count_params()} parameters")
    return model


def get_model(gate_type: str) -> keras.Model:
    """
    Factory function to get model by gate type.

    Args:
        gate_type: Type of gate ("and" or "xor")

    Returns:
        Compiled Keras model

    Raises:
        ValueError: If gate_type is unknown
    """
    gate_type = gate_type.lower()

    if gate_type == "and":
        return create_and_model()
    elif gate_type == "xor":
        return create_xor_model()
    else:
        raise ValueError(f"Unknown gate type: {gate_type}")


if __name__ == "__main__":
    # Test model creation
    from logger_config import setup_logger
    setup_logger()

    print("\n" + "=" * 60)
    print("AND Gate Model")
    print("=" * 60)
    and_model = create_and_model()
    and_model.summary()

    print("\n" + "=" * 60)
    print("XOR Gate Model")
    print("=" * 60)
    xor_model = create_xor_model()
    xor_model.summary()
