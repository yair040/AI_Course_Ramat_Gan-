"""
Iris SVM Classification Package
Author: Yair Levi

A hierarchical SVM classification system for the Iris dataset.
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"

from iris_classifier import config
from iris_classifier import logger_setup
from iris_classifier import data_loader
from iris_classifier import preprocessor
from iris_classifier import svm_trainer
from iris_classifier import evaluator
from iris_classifier import statistics
from iris_classifier import visualizer
from iris_classifier import iteration_runner
from iris_classifier import output_formatter

__all__ = [
    'config',
    'logger_setup',
    'data_loader',
    'preprocessor',
    'svm_trainer',
    'evaluator',
    'statistics',
    'visualizer',
    'iteration_runner',
    'output_formatter'
]