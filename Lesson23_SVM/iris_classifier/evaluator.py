"""
Model evaluation module for Iris classification.
Author: Yair Levi
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, confusion_matrix
)
from iris_classifier.logger_setup import get_logger

logger = get_logger(__name__)


def evaluate_predictions(y_true, y_pred, stage_name=""):
    """
    Evaluate predictions and calculate metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        stage_name: Name of classification stage for logging
    
    Returns:
        dict: Evaluation metrics
    """
    logger.info(f"Evaluating predictions for {stage_name}")
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    
    # Use macro average for multi-class
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Log results
    logger.info(f"{stage_name} Accuracy: {accuracy:.4f}")
    logger.info(f"{stage_name} Precision: {precision:.4f}")
    logger.info(f"{stage_name} Recall: {recall:.4f}")
    logger.info(f"{stage_name} F1-Score: {f1:.4f}")
    logger.info(f"{stage_name} Confusion Matrix:\n{cm}")
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm
    }


def combine_stage_predictions(y_test_original, y_pred_stage1, y_pred_stage2, stage2_indices):
    """
    Combine Stage 1 and Stage 2 predictions into final predictions.
    
    Args:
        y_test_original: Original test labels
        y_pred_stage1: Stage 1 predictions (0 or 1)
        y_pred_stage2: Stage 2 predictions for Group B samples
        stage2_indices: Indices of Group B samples
    
    Returns:
        np.ndarray: Final predictions (0, 1, or 2)
    """
    logger.info("Combining Stage 1 and Stage 2 predictions")
    
    # Initialize final predictions
    final_predictions = np.zeros(len(y_test_original), dtype=int)
    
    # Stage 1 predicted Group A (class 0) → final class 0
    final_predictions[y_pred_stage1 == 0] = 0
    
    # Stage 1 predicted Group B → use Stage 2 predictions
    # Stage 2 classes are 1 and 2 (original labels)
    final_predictions[stage2_indices] = y_pred_stage2
    
    logger.info(f"Final prediction distribution: {np.bincount(final_predictions)}")
    
    return final_predictions