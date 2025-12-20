"""
Data loading and splitting module for Iris dataset.
Author: Yair Levi
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from iris_classifier.logger_setup import get_logger
from iris_classifier.config import DATA_PATH, TRAIN_SPLIT, RANDOM_STATE

logger = get_logger(__name__)


def load_iris_data():
    """
    Load Iris dataset from CSV file.
    
    Returns:
        pd.DataFrame: Loaded dataset
    
    Raises:
        FileNotFoundError: If data file doesn't exist
        ValueError: If data format is invalid
    """
    logger.info(f"Loading data from: {DATA_PATH}")
    
    if not DATA_PATH.exists():
        logger.error(f"Data file not found: {DATA_PATH}")
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")
    
    try:
        df = pd.read_csv(DATA_PATH)
        logger.info(f"Data loaded successfully: {df.shape[0]} samples, {df.shape[1]} features")
        
        # Validate data structure
        if df.empty:
            raise ValueError("Dataset is empty")
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        if missing > 0:
            logger.warning(f"Found {missing} missing values in dataset")
        
        return df
    
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def split_data(X, y, test_size=None, random_state=None):
    """
    Split data into training and testing sets with stratification.
    
    Args:
        X: Features array
        y: Labels array
        test_size: Proportion of test set (default from config)
        random_state: Random seed (default from config)
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    if test_size is None:
        test_size = 1 - TRAIN_SPLIT
    if random_state is None:
        random_state = RANDOM_STATE
    
    logger.info(f"Splitting data: {TRAIN_SPLIT*100:.0f}% train, {test_size*100:.0f}% test")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    
    logger.info(f"Train set: {len(X_train)} samples")
    logger.info(f"Test set: {len(X_test)} samples")
    logger.info(f"Train class distribution: {np.bincount(y_train)}")
    logger.info(f"Test class distribution: {np.bincount(y_test)}")
    
    return X_train, X_test, y_train, y_test