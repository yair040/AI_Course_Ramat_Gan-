"""
Main Program - Perceptron Gates

Author: Yair Levi
Date: 2025-12-30

Main orchestrator for AND and XOR gate neural network training and visualization.
"""

import logging
from pathlib import Path
from multiprocessing import Pool
from typing import Dict, Tuple
import warnings

# Suppress TensorFlow warnings
warnings.filterwarnings("ignore")
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Local imports
from . import logger_config
from . import dataset_generator
from . import models
from . import trainer
from . import visualizer

# Setup logger
logger = logger_config.setup_logger(__name__)


def process_gate(gate_type: str) -> Dict:
    """Complete pipeline for a single gate."""
    import numpy as np
    logger.info(f"\n{'=' * 60}\nProcessing {gate_type.upper()} Gate\n{'=' * 60}")

    try:
        # Generate dataset
        logger.info(f"Generating dataset...")
        dataset = dataset_generator.create_dataset(gate_type, 600, 0.15)

        # Create and train model
        logger.info(f"Creating and training model...")
        model = models.get_model(gate_type)
        history = trainer.train_model(
            model, dataset["X_train"], dataset["y_train"],
            dataset["X_val"], dataset["y_val"], epochs=500, batch_size=32, verbose=0
        )

        # Evaluate
        logger.info(f"Evaluating model...")
        metrics = trainer.evaluate_model(model, dataset["X_val"], dataset["y_val"])

        # Save model
        logger.info(f"Saving model...")
        model_path = Path(__file__).parent / "models" / f"{gate_type}_model.keras"
        trainer.save_model(model, model_path)
        trainer.predict_truth_table(model, gate_type)

        # Visualizations
        logger.info(f"Creating visualizations...")
        viz_dir = Path(__file__).parent / "visualizations"
        visualizer.plot_network_architecture(model, gate_type, viz_dir)
        X_all = np.vstack([dataset["X_train"], dataset["X_val"]])
        y_all = np.concatenate([dataset["y_train"], dataset["y_val"]])
        visualizer.plot_data_points(X_all, y_all, gate_type, viz_dir)
        visualizer.plot_training_history(history, gate_type, viz_dir)

        logger.info(f"{gate_type.upper()} gate processing complete!")
        return {
            "gate_type": gate_type, "success": True,
            "metrics": metrics, "model_path": str(model_path)
        }
    except Exception as e:
        logger.error(f"Error processing {gate_type.upper()}: {e}", exc_info=True)
        return {"gate_type": gate_type, "success": False, "error": str(e)}


def main():
    """Main entry point - orchestrates the entire pipeline."""
    logger.info("\n" + "=" * 70)
    logger.info("Perceptron Gates Neural Network Training - Author: Yair Levi")
    logger.info("=" * 70)

    gates = ["and", "xor"]
    logger.info(f"\nProcessing {len(gates)} gates using multiprocessing...")

    with Pool(processes=len(gates)) as pool:
        results = pool.map(process_gate, gates)

    logger.info("\n" + "=" * 70 + "\nSUMMARY\n" + "=" * 70)
    for result in results:
        gate = result["gate_type"].upper()
        if result["success"]:
            m = result["metrics"]
            logger.info(
                f"{gate}: ✓ SUCCESS - Acc: {m['accuracy']:.2%}, "
                f"Loss: {m['loss']:.4f}, Model: {result['model_path']}"
            )
        else:
            logger.info(f"{gate}: ✗ FAILED - {result['error']}")
    logger.info("=" * 70 + "\nAll tasks completed!\n" + "=" * 70)


if __name__ == "__main__":
    main()
