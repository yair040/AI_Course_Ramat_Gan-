"""
Iris Naive Bayes Classification Package

This package implements Naive Bayes classification for the Iris flower dataset
using both manual (NumPy-based) and library-based (scikit-learn) approaches.

Author: Yair Levi
Date: 2025-12-03
Version: 1.0.0
"""

from .data_loader import get_data, load_iris_data, split_data
from .naive_bayes_manual import ManualNaiveBayes
from .naive_bayes_library import LibraryNaiveBayes
from .visualization import plot_histograms, plot_confusion_matrix, display_results
from .logger_config import setup_logger

__version__ = '1.0.0'
__author__ = 'Yair Levi'

__all__ = [
    'get_data',
    'load_iris_data',
    'split_data',
    'ManualNaiveBayes',
    'LibraryNaiveBayes',
    'plot_histograms',
    'plot_confusion_matrix',
    'display_results',
    'setup_logger'
]
