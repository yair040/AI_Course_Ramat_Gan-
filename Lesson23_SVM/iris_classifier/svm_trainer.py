"""
SVM training module for Iris classification.
Author: Yair Levi
"""

import time
from sklearn.svm import SVC
from iris_classifier.logger_setup import get_logger
from iris_classifier.config import SVM_KERNEL, SVM_C, SVM_GAMMA

logger = get_logger(__name__)


def train_svm(X_train, y_train, kernel=None, C=None, gamma=None, class_weight=None):
    """
    Train SVM classifier.
    
    Args:
        X_train: Training features
        y_train: Training labels
        kernel: SVM kernel type (default from config)
        C: Regularization parameter (default from config)
        gamma: Kernel coefficient (default from config)
        class_weight: Class weights for imbalanced data (default None)
    
    Returns:
        SVC: Trained SVM model
    """
    # Use defaults from config if not specified
    if kernel is None:
        kernel = SVM_KERNEL
    if C is None:
        C = SVM_C
    if gamma is None:
        gamma = SVM_GAMMA
    
    logger.info(f"Training SVM: kernel={kernel}, C={C}, gamma={gamma}, class_weight={class_weight}")
    logger.info(f"Training samples: {len(X_train)}, Features: {X_train.shape[1]}")
    
    # Create and train SVM
    start_time = time.time()
    
    model = SVC(kernel=kernel, C=C, gamma=gamma, random_state=42, class_weight=class_weight)
    
    try:
        model.fit(X_train, y_train)
        training_time = time.time() - start_time
        
        logger.info(f"SVM training completed in {training_time:.3f} seconds")
        logger.info(f"Support vectors: {model.n_support_}")
        
        return model
    
    except Exception as e:
        logger.error(f"SVM training failed: {e}")
        raise


def predict_svm(model, X_test):
    """
    Make predictions using trained SVM model.
    
    Args:
        model: Trained SVM model
        X_test: Test features
    
    Returns:
        np.ndarray: Predictions
    """
    logger.info(f"Making predictions on {len(X_test)} test samples")
    
    try:
        predictions = model.predict(X_test)
        logger.info(f"Predictions complete: {len(predictions)} samples")
        return predictions
    
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise