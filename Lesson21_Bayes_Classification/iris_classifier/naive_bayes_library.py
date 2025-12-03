"""
Library-based Naive Bayes Implementation

Uses scikit-learn's GaussianNB for Naive Bayes classification.
Serves as validation for the manual implementation.

Author: Yair Levi
"""

import logging
from sklearn.naive_bayes import GaussianNB


logger = logging.getLogger('iris_classifier')


class LibraryNaiveBayes:
    """
    Wrapper class for scikit-learn's Gaussian Naive Bayes classifier.

    Uses Gaussian distribution assumption for continuous features.
    """

    def __init__(self):
        """
        Initialize Library-based Naive Bayes classifier.
        """
        self.model = GaussianNB()
        logger.info("LibraryNaiveBayes initialized with GaussianNB")

    def fit(self, X_train, y_train):
        """
        Train the Gaussian Naive Bayes classifier.

        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,)

        Returns:
            self
        """
        logger.info("Starting library Naive Bayes training")
        self.model.fit(X_train, y_train)
        logger.info("Library Naive Bayes training completed")
        return self

    def predict(self, X_test):
        """
        Predict class labels for test samples.

        Args:
            X_test: Test features (n_samples, n_features)

        Returns:
            Predicted labels (n_samples,)
        """
        logger.info(f"Predicting labels for {len(X_test)} test samples")
        predictions = self.model.predict(X_test)
        logger.info("Prediction completed")
        return predictions

    def get_model(self):
        """
        Get the underlying scikit-learn model.

        Returns:
            GaussianNB model instance
        """
        return self.model
