"""
Lost in the Middle - Context Window Testing Framework

This package tests the hypothesis that Large Language Models (LLMs) have
lower accuracy in retrieving information from the middle portions of long
documents compared to information at the beginning or end.

Author: Yair Levi
Version: 1.0
Date: 2025-12-10

Modules:
    config: Configuration constants and settings
    utils: Utility functions for logging and setup
    document_generator: Generate test documents
    sentence_injector: Inject test sentences at different positions
    api_tester: Test documents using Anthropic API
    analyzer: Statistical analysis of results
    visualizer: Visualization of results
    main: Main program execution

Usage:
    python main.py
"""

__version__ = "1.0.0"
__author__ = "Yair Levi"
__all__ = [
    "config",
    "utils",
    "document_generator",
    "sentence_injector",
    "api_tester",
    "analyzer",
    "visualizer",
    "main"
]
