"""
Manual Naive Bayes Implementation using NumPy

Implements Naive Bayes classification from scratch using only NumPy.
Uses histogram-based probability estimation with Laplace smoothing.

Author: Yair Levi
"""

import numpy as np
import logging
from multiprocessing import Pool, cpu_count


logger = logging.getLogger('iris_classifier')


def _build_single_histogram(args):
    """Worker function for parallel histogram building."""
    class_name, feature_idx, feature_data, n_bins = args

    # Build histogram
    counts, bin_edges = np.histogram(feature_data, bins=n_bins)

    # Apply Laplace smoothing (add 1 to all bins, including empty ones)
    counts = counts + 1

    return (class_name, feature_idx, counts, bin_edges)


class ManualNaiveBayes:
    """
    Manual implementation of Naive Bayes classifier using NumPy.

    Uses histogram-based probability estimation for continuous features.
    Implements logarithmic Naive Bayes to avoid numerical underflow.
    """

    def __init__(self, n_bins=10):
        """
        Initialize Manual Naive Bayes classifier.

        Args:
            n_bins: Number of bins for histogram (default: 10)
        """
        self.n_bins = n_bins
        self.priors = {}  # P(Ci) for each class
        self.histograms = {}  # {class: {feature_idx: (counts, edges)}}
        self.classes = None
        self.n_features = None
        logger.info(f"ManualNaiveBayes initialized with n_bins={n_bins}")

    def fit(self, X_train, y_train):
        """
        Train the Naive Bayes classifier.

        Calculates prior probabilities and builds histograms for each
        class-feature combination using multiprocessing.

        Args:
            X_train: Training features (n_samples, n_features)
            y_train: Training labels (n_samples,)

        Returns:
            self
        """
        logger.info("Starting manual Naive Bayes training")

        self.classes = np.unique(y_train)
        self.n_features = X_train.shape[1]
        n_samples = len(y_train)

        # Calculate prior probabilities P(Ci)
        logger.info("Calculating prior probabilities")
        for class_name in self.classes:
            class_count = np.sum(y_train == class_name)
            self.priors[class_name] = class_count / n_samples
            logger.info(f"P({class_name}) = {self.priors[class_name]:.4f}")

        # Build histograms using multiprocessing
        logger.info("Building histograms with multiprocessing")
        self._build_histograms_parallel(X_train, y_train)

        logger.info("Manual Naive Bayes training completed")
        return self

    def _build_histograms_parallel(self, X_train, y_train):
        """Build histograms for all class-feature combinations in parallel."""
        # Prepare tasks for parallel processing
        tasks = []
        for class_name in self.classes:
            for feature_idx in range(self.n_features):
                # Extract feature data for this class
                feature_data = X_train[y_train == class_name, feature_idx]
                tasks.append((class_name, feature_idx, feature_data, self.n_bins))

        # Use multiprocessing to build histograms
        n_workers = min(cpu_count(), len(tasks))
        logger.info(f"Building {len(tasks)} histograms using {n_workers} workers")

        with Pool(n_workers) as pool:
            results = pool.map(_build_single_histogram, tasks)

        # Organize results into nested dictionary
        for class_name, feature_idx, counts, bin_edges in results:
            if class_name not in self.histograms:
                self.histograms[class_name] = {}
            self.histograms[class_name][feature_idx] = (counts, bin_edges)

        logger.info("Histogram building completed")

    def predict(self, X_test):
        """
        Predict class labels for test samples.

        Uses logarithmic Naive Bayes formula:
        P(Ci|X) = log(P(Ci)) + Σ log(P(Xi|Ci))

        Args:
            X_test: Test features (n_samples, n_features)

        Returns:
            Predicted labels (n_samples,)
        """
        logger.info(f"Predicting labels for {len(X_test)} test samples")

        predictions = []

        for sample_idx, sample in enumerate(X_test):
            class_probs = {}

            # Calculate log probability for each class
            for class_name in self.classes:
                # Start with log prior
                log_prob = np.log(self.priors[class_name])

                # Add log likelihood for each feature
                for feature_idx in range(self.n_features):
                    feature_value = sample[feature_idx]
                    p_xi_given_ci = self._get_feature_probability(
                        feature_value, class_name, feature_idx
                    )
                    log_prob += np.log(p_xi_given_ci)

                class_probs[class_name] = log_prob

            # Assign class with highest probability
            predicted_class = max(class_probs, key=class_probs.get)
            predictions.append(predicted_class)

        predictions = np.array(predictions)
        logger.info("Prediction completed")
        return predictions

    def _get_feature_probability(self, feature_value, class_name, feature_idx):
        """Calculate P(Xi|Ci) for a feature value given a class."""
        counts, bin_edges = self.histograms[class_name][feature_idx]

        # Find which bin the feature value falls into
        bin_idx = np.digitize(feature_value, bin_edges) - 1

        # Handle edge cases
        if bin_idx < 0:
            bin_idx = 0
        elif bin_idx >= len(counts):
            bin_idx = len(counts) - 1

        # Calculate probability: bin_count / total_count
        total_count = np.sum(counts)
        probability = counts[bin_idx] / total_count

        return probability

    def get_histograms(self):
        """Get histogram data for visualization."""
        return self.histograms
