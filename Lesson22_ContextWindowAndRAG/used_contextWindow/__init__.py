"""
Context Window Size Impact Testing Package

Tests the hypothesis that LLM search accuracy degrades as context window size increases.

This package generates documents of varying sizes (2K-50K words), queries them via
the Anthropic API using Claude Haiku 4.5, and measures accuracy and performance.

Usage:
    python -m context_window_test

    Or in Python:
    >>> from context_window_test import main
    >>> main()

Author: Yair Levi
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__email__ = "yair0@example.com"

# Define public API
__all__ = [
    "__version__",
    "__author__"
]
