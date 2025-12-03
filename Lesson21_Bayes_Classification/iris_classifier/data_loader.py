"""
Data Loading and Preprocessing Module

Loads iris.csv dataset and splits into training and test sets.

Author: Yair Levi
"""

import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
import logging


logger = logging.getLogger('iris_classifier')


def load_iris_data(file_path='iris.csv'):
    """
    Load iris dataset from CSV file.

    Args:
        file_path: Relative path to CSV file (default: 'iris.csv')

    Returns:
        pandas DataFrame with iris data

    Raises:
        FileNotFoundError: If CSV file not found
        ValueError: If CSV format is invalid
    """
    # Get project root and construct path
    project_root = Path(__file__).parent.parent
    data_path = project_root / file_path

    logger.info(f"Loading data from: {data_path}")

    if not data_path.exists():
        error_msg = f"Data file not found: {data_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Load CSV
    try:
        data = pd.read_csv(data_path)
        logger.info(f"Data loaded successfully. Shape: {data.shape}")
    except Exception as e:
        error_msg = f"Error reading CSV: {e}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Validate structure (should have 5 columns: 4 features + 1 label)
    if data.shape[1] != 5:
        error_msg = f"Expected 5 columns, got {data.shape[1]}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"Data validation passed. Columns: {list(data.columns)}")
    return data


def split_data(data, test_size=0.25, random_state=42):
    """
    Split dataset into training and test sets.

    Args:
        data: pandas DataFrame with features and label
        test_size: Proportion of data for test set (default: 0.25)
        random_state: Random seed for reproducibility (default: 42)

    Returns:
        Tuple of (X_train, X_test, y_train, y_test)
    """
    logger.info(f"Splitting data: test_size={test_size}, random_state={random_state}")

    # Separate features (first 4 columns) and labels (last column)
    X = data.iloc[:, :-1].values  # All rows, first 4 columns
    y = data.iloc[:, -1].values   # All rows, last column

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(f"Training set size: {len(X_train)} samples")
    logger.info(f"Test set size: {len(X_test)} samples")
    logger.info(f"Training class distribution: {np.unique(y_train, return_counts=True)}")
    logger.info(f"Test class distribution: {np.unique(y_test, return_counts=True)}")

    return X_train, X_test, y_train, y_test


def get_data(file_path='iris.csv', test_size=0.25, random_state=42):
    """
    Main function to load and prepare all data.

    Args:
        file_path: Path to CSV file
        test_size: Proportion for test set
        random_state: Random seed

    Returns:
        Dictionary containing:
            - X_train, X_test, y_train, y_test: Split data
            - feature_names: List of feature column names
            - class_names: List of unique class labels
            - n_features: Number of features
            - n_classes: Number of classes
    """
    logger.info("Starting data loading and preprocessing")

    # Load data
    data = load_iris_data(file_path)

    # Extract metadata
    feature_names = list(data.columns[:-1])
    class_names = sorted(data.iloc[:, -1].unique())

    logger.info(f"Feature names: {feature_names}")
    logger.info(f"Class names: {class_names}")

    # Split data
    X_train, X_test, y_train, y_test = split_data(data, test_size, random_state)

    # Prepare return dictionary
    result = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'feature_names': feature_names,
        'class_names': class_names,
        'n_features': len(feature_names),
        'n_classes': len(class_names)
    }

    logger.info("Data loading and preprocessing completed successfully")
    return result
