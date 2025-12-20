"""
Task module for Stage 1 classification.
Stage 1: Classify Group A (class 0) vs Group B (classes 1,2)
Author: Yair Levi
"""

import numpy as np
from iris_classifier.logger_setup import get_logger
from iris_classifier.data_loader import load_iris_data, split_data
from iris_classifier.preprocessor import normalize_features, group_classes_stage1
from iris_classifier.svm_trainer import train_svm, predict_svm
from iris_classifier.evaluator import evaluate_predictions

logger = get_logger(__name__)


def run_stage1(iteration_num):
    """
    Execute Stage 1 classification: Group A vs Group B.
    
    Args:
        iteration_num: Current iteration number
    
    Returns:
        dict: Stage 1 results including model, predictions, and metrics
    """
    logger.info(f"="*60)
    logger.info(f"ITERATION {iteration_num + 1} - STAGE 1: Group A vs Group B")
    logger.info(f"="*60)
    
    try:
        # Load data
        df = load_iris_data()
        
        # Assume last column is target, rest are features
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        
        # Convert target to integers if needed
        if y.dtype == object:
            # Map class names to integers
            unique_classes = np.unique(y)
            class_mapping = {cls: i for i, cls in enumerate(unique_classes)}
            y = np.array([class_mapping[cls] for cls in y])
            logger.info(f"Class mapping: {class_mapping}")
        
        # Split data with iteration-specific random state for variety
        X_train, X_test, y_train_orig, y_test_orig = split_data(
            X, y, random_state=42 + iteration_num
        )
        
        # Group classes for Stage 1
        y_train_stage1 = group_classes_stage1(y_train_orig)
        y_test_stage1 = group_classes_stage1(y_test_orig)
        
        # Normalize features
        X_train_norm, X_test_norm, scaler = normalize_features(X_train, X_test)
        
        # Train SVM
        model = train_svm(X_train_norm, y_train_stage1)
        
        # Predict
        y_pred_stage1 = predict_svm(model, X_test_norm)
        
        # Evaluate
        metrics = evaluate_predictions(y_test_stage1, y_pred_stage1, "Stage 1")
        
        logger.info(f"Stage 1 completed successfully")
        
        return {
            'model': model,
            'predictions': y_pred_stage1,
            'test_data': (X_test_norm, y_test_orig),
            'train_data': (X_train, y_train_orig),  # Pass for Stage 2 consistency
            'metrics': metrics,
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1_score'],
            'confusion_matrix': metrics['confusion_matrix']
        }
    
    except Exception as e:
        logger.error(f"Stage 1 failed for iteration {iteration_num + 1}: {e}")
        raise