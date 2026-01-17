"""
Balanced Token Tree Package

A Python package for creating and balancing binary trees with token distribution.
The package demonstrates tree balancing algorithms using a 5-level BST structure
with visualization capabilities.

Author: Yair Levi
Date: 2026-01-15
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__license__ = "MIT"

# Import main components for convenient access
from .tree_structure import TreeNode, BinaryTree, build_tree
from .tasks import run_pipeline
from .logger_config import setup_logging

__all__ = [
    "TreeNode",
    "BinaryTree",
    "build_tree",
    "run_pipeline",
    "setup_logging",
    "__version__",
    "__author__",
]
