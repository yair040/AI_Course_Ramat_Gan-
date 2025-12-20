"""
Data preprocessing module for Iris classification.
Author: Yair Levi
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from iris_classifier.logger_setup import get_logger
from iris_classifier.config import STAGE1_GROUP_A, STAGE1_GROUP_B

logger = get_logger(__name__)


def normalize_features(X_train, X_test):
    """
    Normalize features using StandardScaler.
    
    Args:
        X_train: Training features
        X_test: Testing features
    
    Returns:
        tuple: (X_train_scaled, X_test_scaled, scaler)
    """
    logger.info("Normalizing features with StandardScaler")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info(f"Feature scaling complete - Mean: {scaler.mean_}, Std: {scaler.scale_}")
    
    return X_train_scaled, X_test_scaled, scaler


def group_classes_stage1(y):
    """
    Group classes for Stage 1: {0} vs {1,2}
    
    Args:
        y: Original class labels (0, 1, 2)
    
    Returns:
        np.ndarray: Binary labels (0 for Group A, 1 for Group B)
    """
    logger.info(f"Grouping classes for Stage 1: {STAGE1_GROUP_A} vs {STAGE1_GROUP_B}")
    
    y_grouped = np.zeros_like(y)
    
    # Group A: class 0 → label 0
    y_grouped[np.isin(y, STAGE1_GROUP_A)] = 0
    
    # Group B: classes 1,2 → label 1
    y_grouped[np.isin(y, STAGE1_GROUP_B)] = 1
    
    logger.info(f"Stage 1 class distribution: {np.bincount(y_grouped)}")
    
    return y_grouped


def filter_group_b(X, y, y_pred_stage1):
    """
    Filter samples predicted as Group B for Stage 2 classification.
    
    Args:
        X: Features
        y: Original labels
        y_pred_stage1: Stage 1 predictions
    
    Returns:
        tuple: (X_filtered, y_filtered, indices)
    """
    # Get indices where Stage 1 predicted Group B (label 1)
    group_b_mask = (y_pred_stage1 == 1)
    indices = np.where(group_b_mask)[0]
    
    X_filtered = X[group_b_mask]
    y_filtered = y[group_b_mask]
    
    logger.info(f"Filtered {len(X_filtered)} Group B samples for Stage 2")
    logger.info(f"Stage 2 class distribution: {np.bincount(y_filtered)}")
    
    return X_filtered, y_filtered, indices