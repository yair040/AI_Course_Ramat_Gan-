"""
Training Module

Author: Yair Levi
Date: 2025-12-30

Handles model training, evaluation, and persistence.
"""

import logging
import numpy as np
from pathlib import Path
from typing import Dict, Tuple
from tensorflow import keras

logger = logging.getLogger(__name__)


def train_model(
    model: keras.Model,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    epochs: int = 500,
    batch_size: int = 32,
    verbose: int = 0
) -> keras.callbacks.History:
    """Train a Keras model with training and validation data."""
    logger.info(f"Training {model.name}: {len(X_train)} train, {len(X_val)} val, {epochs} epochs")

    history = model.fit(
        X_train, y_train, validation_data=(X_val, y_val),
        epochs=epochs, batch_size=batch_size, verbose=verbose
    )

    h = history.history
    logger.info(
        f"{model.name} done - Loss: {h['loss'][-1]:.4f}, Acc: {h['accuracy'][-1]:.4f}, "
        f"Val Loss: {h['val_loss'][-1]:.4f}, Val Acc: {h['val_accuracy'][-1]:.4f}"
    )
    return history


def evaluate_model(
    model: keras.Model,
    X_test: np.ndarray,
    y_test: np.ndarray
) -> Dict[str, float]:
    """Evaluate model performance on test data."""
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    logger.info(f"{model.name} evaluation - Loss: {loss:.4f}, Accuracy: {accuracy:.4f}")
    return {"loss": float(loss), "accuracy": float(accuracy)}


def save_model(model: keras.Model, filepath: Path) -> None:
    """Save trained model to file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    model.save(filepath)
    logger.info(f"Model saved to: {filepath}")


def load_model(filepath: Path) -> keras.Model:
    """Load a trained model from file."""
    model = keras.models.load_model(filepath)
    logger.info(f"Model loaded from: {filepath}")
    return model


def predict_truth_table(model: keras.Model, gate_type: str) -> None:
    """Test model predictions on the original truth table."""
    truth_inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=np.float32)
    predictions = model.predict(truth_inputs, verbose=0)

    logger.info(f"\n{gate_type.upper()} Gate Predictions:")
    logger.info("Input | Prediction | Rounded")
    logger.info("-" * 35)
    for inp, pred in zip(truth_inputs, predictions):
        logger.info(f"{inp} | {pred[0]:.4f}    | {round(pred[0])}")
