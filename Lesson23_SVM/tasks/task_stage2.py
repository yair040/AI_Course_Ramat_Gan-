"""
Task module for Stage 2 classification.
Stage 2: Classify classes 1 vs 2 within Group B
Author: Yair Levi
"""

import numpy as np
from iris_classifier.logger_setup import get_logger
from iris_classifier.data_loader import load_iris_data, split_data
from iris_classifier.preprocessor import normalize_features
from iris_classifier.svm_trainer import train_svm, predict_svm
from iris_classifier.evaluator import evaluate_predictions

logger = get_logger(__name__)


def run_stage2(iteration_num, stage1_results):
    """
    Execute Stage 2 classification: Separate classes 1 and 2.
    
    Args:
        iteration_num: Current iteration number
        stage1_results: Results from Stage 1
    
    Returns:
        dict: Stage 2 results including predictions and metrics
    """
    logger.info(f"="*60)
    logger.info(f"ITERATION {iteration_num + 1} - STAGE 2: Class 1 vs Class 2")
    logger.info(f"="*60)
    
    try:
        # Get Stage 1 predictions to know which test samples are in Group B
        y_pred_stage1 = stage1_results['predictions']
        
        # Reload data with SAME random state to get consistent split
        df = load_iris_data()
        X = df.iloc[:, :-1].values
        y = df.iloc[:, -1].values
        
        # Convert target to integers if needed
        if y.dtype == object:
            unique_classes = np.unique(y)
            class_mapping = {cls: i for i, cls in enumerate(unique_classes)}
            y = np.array([class_mapping[cls] for cls in y])
            logger.info(f"Class mapping: {class_mapping}")
        
        # Split with SAME random state as Stage 1
        X_train, X_test, y_train, y_test = split_data(
            X, y, random_state=42 + iteration_num
        )
        
        # TRAINING: Filter to only Group B samples (classes 1 and 2)
        train_group_b_mask = np.isin(y_train, [1, 2])
        X_train_group_b = X_train[train_group_b_mask]
        y_train_group_b = y_train[train_group_b_mask]
        
        logger.info(f"Training set - Group B samples: {len(X_train_group_b)}")
        logger.info(f"Training set - Class distribution: {np.bincount(y_train_group_b)}")
        
        # TEST: Filter to only samples that Stage 1 predicted as Group B
        test_group_b_mask = (y_pred_stage1 == 1)
        X_test_group_b = X_test[test_group_b_mask]
        y_test_group_b = y_test[test_group_b_mask]
        group_b_indices = np.where(test_group_b_mask)[0]
        
        logger.info(f"Test set - Predicted as Group B: {len(X_test_group_b)}")
        logger.info(f"Test set - Actual class distribution: {np.bincount(y_test_group_b)}")
        
        if len(X_test_group_b) == 0:
            logger.warning("No Group B samples to classify in Stage 2")
            return _empty_stage2_result()
        
        # Normalize features - fit on training Group B, transform both train and test
        X_train_norm, X_test_norm, scaler = normalize_features(
            X_train_group_b, X_test_group_b
        )
        
        logger.info("Features normalized for Stage 2")
        
        # Train SVM on normalized Group B training data
        # Use class_weight='balanced' to handle any class imbalance
        model = train_svm(
            X_train_norm, y_train_group_b, 
            C=1.0, gamma='scale', class_weight='balanced'
        )
        
        # Predict on normalized Group B test data
        y_pred_stage2 = predict_svm(model, X_test_norm)
        
        logger.info(f"Stage 2 predictions distribution: {np.bincount(y_pred_stage2)}")
        
        # Evaluate Stage 2
        metrics = evaluate_predictions(y_test_group_b, y_pred_stage2, "Stage 2")
        
        logger.info(f"Stage 2 completed successfully")
        
        return {
            'model': model,
            'predictions': y_pred_stage2,
            'group_b_indices': group_b_indices,
            'metrics': metrics,
            'accuracy': metrics['accuracy'],
            'precision': metrics['precision'],
            'recall': metrics['recall'],
            'f1_score': metrics['f1_score'],
            'confusion_matrix': metrics['confusion_matrix']
        }
    
    except Exception as e:
        logger.error(f"Stage 2 failed for iteration {iteration_num + 1}: {e}", exc_info=True)
        raise


def _empty_stage2_result():
    """Return empty result when no Group B samples."""
    return {
        'predictions': np.array([]),
        'group_b_indices': np.array([]),
        'metrics': {},
        'accuracy': 0.0,
        'precision': 0.0,
        'recall': 0.0,
        'f1_score': 0.0,
        'confusion_matrix': np.array([[]])
    }